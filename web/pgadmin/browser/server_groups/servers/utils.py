##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2020, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

"""Server helper utilities"""
import os


import paramiko


from pgadmin.utils.crypto import encrypt, decrypt
import config
from pgadmin.model import db, Server
from pgadmin.tools.scripts.ssh_utils import SSHClient
from pgadmin.utils import get_storage_directory
from pgadmin.utils.crypto import decrypt
from pgadmin.utils.master_password import get_crypt_key


def parse_priv_from_db(db_privileges):
    """
    Common utility function to parse privileges retrieved from database.
    """
    acl = {
        'grantor': db_privileges['grantor'],
        'grantee': db_privileges['grantee'],
        'privileges': [],
        # 'cluster': db_privileges['cluster'],
        'cluster': db_privileges.setdefault('cluster', ''),
    }

    privileges = []
    for idx, priv in enumerate(db_privileges['privileges']):
        privileges.append({
            "privilege_type": priv,
            "privilege": True,
            "with_grant": db_privileges['grantable'][idx]
        })

    acl['privileges'] = privileges

    return acl


def parse_priv_to_db(str_privileges, allowed_acls=[]):
    """
    Common utility function to parse privileges before sending to database.
    """
    from pgadmin.utils.driver import get_driver
    from config import PG_DEFAULT_DRIVER
    driver = get_driver(PG_DEFAULT_DRIVER)

    db_privileges = {
        'c': 'CONNECT',
        'C': 'CREATE',
        'T': 'TEMPORARY',
        'a': 'INSERT',
        'r': 'SELECT',
        'w': 'UPDATE',
        'D': 'TRUNCATE',
        'x': 'REFERENCES',
        't': 'TRIGGER',
        'U': 'USAGE',
        'X': 'EXECUTE',
        'A': 'ALTER',
        'd': 'DROP',
        's': 'SHOW',
    }

    privileges = []
    allowed_acls_len = len(allowed_acls)

    for priv in str_privileges:
        priv_with_grant = []
        priv_without_grant = []
        cluster = []

        if isinstance(priv['privileges'], dict) \
                and 'changed' in priv['privileges']:
            tmp = []
            for p in priv['privileges']['changed']:
                tmp_p = {'privilege_type': p['privilege_type'],
                         'privilege': False,
                         'with_grant': False}

                if 'with_grant' in p:
                    tmp_p['privilege'] = True
                    tmp_p['with_grant'] = p['with_grant']

                if 'privilege' in p:
                    tmp_p['privilege'] = p['privilege']

                tmp.append(tmp_p)

            priv['privileges'] = tmp

        for privilege in priv['privileges']:

            if privilege['privilege_type'] not in db_privileges:
                continue

            if privilege['privilege_type'] not in allowed_acls:
                continue

            if privilege['with_grant']:
                priv_with_grant.append(
                    db_privileges[privilege['privilege_type']]
                )
            elif privilege['privilege']:
                priv_without_grant.append(
                    db_privileges[privilege['privilege_type']]
                )
        cluster = priv.setdefault('cluster')

        # If we have all acl then just return all
        if len(priv_with_grant) == allowed_acls_len > 1:
            priv_with_grant = ['ALL']
        if len(priv_without_grant) == allowed_acls_len > 1:
            priv_without_grant = ['ALL']
        # Appending and returning all ACL
        privileges.append({
            'grantee': driver.qtIdent(None, priv['grantee'])
            if priv['grantee'] != 'PUBLIC' else 'PUBLIC',
            'with_grant': priv_with_grant,
            'without_grant': priv_without_grant,
            'cluster': cluster
        })

    return privileges


def tokenize_options(options_from_db, option_name, option_value):
    """
    This function will tokenize the string stored in database
    e.g. database store the value as below
    key1=value1, key2=value2, key3=value3, ....
    This function will extract key and value from above string

    Args:
        options_from_db: Options from database
        option_name: Option Name
        option_value: Option Value

    Returns:
        Tokenized options
    """
    options = []
    if options_from_db is not None:
        option_str = options_from_db.split(',')
        for fdw_option in option_str:
            k, v = fdw_option.split('=', 1)
            options.append({option_name: k, option_value: v})
    return options


def validate_options(options, option_name, option_value):
    """
    This function will filter validated options
    and sets flag to use in sql template if there are any
    valid options

    Args:
        options: List of options
        option_name: Option Name
        option_value: Option Value

    Returns:
        Flag, Filtered options
    """
    valid_options = []
    is_valid_options = False

    for option in options:
        # If option name is valid
        if option_name in option and \
            option[option_name] is not None and \
                option[option_name] != '' and \
                len(option[option_name].strip()) > 0:
            # If option value is valid
            if option_value in option and \
                option[option_value] is not None and \
                option[option_value] != '' and \
                    len(option[option_value].strip()) > 0:
                # Do nothing here
                pass
            else:
                # Set empty string if no value provided
                option[option_value] = ''
            valid_options.append(option)

    if len(valid_options) > 0:
        is_valid_options = True

    return is_valid_options, valid_options


def reencrpyt_server_passwords(user_id, old_key, new_key):
    """
    This function will decrypt the saved passwords in SQLite with old key
    and then encrypt with new key
    """
    from pgadmin.utils.driver import get_driver
    driver = get_driver(config.PG_DEFAULT_DRIVER)

    for server in Server.query.filter_by(user_id=user_id).all():
        manager = driver.connection_manager(server.id)

        # Check if old password was stored in pgadmin4 sqlite database.
        # If yes then update that password.
        if server.password is not None:
            password = decrypt(server.password, old_key)

            if isinstance(password, bytes):
                password = password.decode()

            password = encrypt(password, new_key)
            setattr(server, 'password', password)
            manager.password = password
        elif manager.password is not None:
            password = decrypt(manager.password, old_key)

            if isinstance(password, bytes):
                password = password.decode()

            password = encrypt(password, new_key)
            manager.password = password

        if server.tunnel_password is not None:
            tunnel_password = decrypt(server.tunnel_password, old_key)
            if isinstance(tunnel_password, bytes):
                tunnel_password = tunnel_password.decode()

            tunnel_password = encrypt(tunnel_password, new_key)
            setattr(server, 'tunnel_password', tunnel_password)
            manager.tunnel_password = tunnel_password
        elif manager.tunnel_password is not None:
            tunnel_password = decrypt(manager.tunnel_password, old_key)

            if isinstance(tunnel_password, bytes):
                tunnel_password = tunnel_password.decode()

            tunnel_password = encrypt(tunnel_password, new_key)
            manager.tunnel_password = tunnel_password

        db.session.commit()
        manager.update_session()


def remove_saved_passwords(user_id):
    """
    This function will remove all the saved passwords for the server
    """

    try:
        db.session.query(Server) \
            .filter(Server.user_id == user_id) \
            .update({Server.password: None, Server.tunnel_password: None})
        db.session.commit()
    except Exception as _:
        db.session.rollback()
        raise


def get_ssh_client(host, user, port=22, password=None, pkey=None, ):
    ssh_client = SSHClient(host, user, port=port,
                           password=password, pkey=pkey)

    return ssh_client


def _get_ssh_info(gid, sid):
    """
    This function is used to get ssh connection information
    :param gid:
    :param sid:
    :return: ssh_data or None
    """
    # Fetch Server Details
    server = Server.query.filter_by(id=sid).first()
    if server is None:
        return bad_request(gettext("Server not found."))

    # if current_user and hasattr(current_user, 'id'):
    #     # Fetch User Details.
    #     user = User.query.filter_by(id=current_user.id).first()
    #     if user is None:
    #         return unauthorized(gettext("Unauthorized request."))
    # else:
    #     return unauthorized(gettext("Unauthorized request."))

    # data = request.form if request.form else json.loads(
    #     request.data, encoding='utf-8'
    # ) if request.data else {}
    data = dict()

    ssh_data = dict()
    # Connect the Server
    # manager = get_driver(PG_DEFAULT_DRIVER).connection_manager(sid)
    # conn = manager.connection()

    # Get enc key
    crypt_key_present, crypt_key = get_crypt_key()
    if not crypt_key_present:
        raise CryptKeyMissing

    if 'ssh_username' not in data:
        ssh_data['ssh_username'] = server.ssh_username
    else:
        ssh_data['ssh_username'] = data['ssh_usernmae']

    if 'ssh_port' not in data:
        ssh_data['ssh_port'] = server.ssh_port
    else:
        ssh_data['ssh_port'] = data['ssh_port']

    if 'host' not in data:
        ssh_data['host'] = server.host
    else:
        ssh_data['host'] = data['host']

    if 'ssh_authentication_type' not in data:
        ssh_data['ssh_authentication_type'] = int(server.ssh_authentication_type)
    else:
        ssh_data['ssh_authentication_type'] = int(data['ssh_authentication_type'])

    if ssh_data['ssh_authentication_type'] == 1:
        # get ssh key file path and user email for generate an absolute path
        if 'ssh_key_file' not in data:
            ssh_data['ssh_key_file'] = server.ssh_key_file
        else:
            ssh_data['ssh_key_file'] = data['ssh_key_file']

        if ssh_data['ssh_key_file'].startswith('/'):
            ssh_data['ssh_key_file'] = ssh_data['ssh_key_file'][1:]
        # retrieve ssh key directory path
        storage_path = get_storage_directory()
        if storage_path:
            # generate full path of ssh key file
            ssh_data['ssh_key_path'] = os.path.join(
                storage_path,
                ssh_data['ssh_key_file'].lstrip('/').lstrip('\\')
            )
            ssh_data['private_key'] = paramiko.RSAKey.from_private_key_file(
                ssh_data['ssh_key_path'])
        ssh_data['ssh_password'] = None

    if ssh_data['ssh_authentication_type'] == 0:
        if 'ssh_password' not in data:
            decrypted_password = decrypt(server.ssh_password, crypt_key)

            if isinstance(decrypted_password, bytes):
                decrypted_password = decrypted_password.decode()

            ssh_data['ssh_password'] = decrypted_password
        else:
            ssh_data['ssh_password'] = data['ssh_password']
        ssh_data['private_key'] = None

    if ssh_data['ssh_username'] is None \
       or (
           ssh_data['private_key'] is None
           and ssh_data['ssh_password'] is None
    ):

        ssh_data = None

    return ssh_data


def get_ssh_info(gid, sid):
    """
    This function is used to get ssh connection information
    :param gid:
    :param sid:
    :return: ssh_data or None
    """
    # Fetch Server Details
    server = Server.query.filter_by(id=sid).first()
    if server is None:
        return bad_request(gettext("Server not found."))

    # Get enc key
    crypt_key_present, crypt_key = get_crypt_key()
    if not crypt_key_present:
        raise CryptKeyMissing

    ssh_data = dict()

    ssh_data['host'] = server.host
    ssh_data['ssh_username'] = server.ssh_username
    ssh_data['ssh_port'] = server.ssh_port
    ssh_data['ssh_authentication_type'] = int(server.ssh_authentication_type)
    ssh_data['ssh_key_file'] = server.ssh_key_file
    ssh_data['ssh_password'] = server.ssh_password

    if not server.ssh_username \
       or (not server.ssh_key_file and not server.ssh_password) \
       or (int(server.ssh_authentication_type) == 0 and not server.ssh_password):
        ssh_data = None
    elif ssh_data['ssh_authentication_type'] == 0:
        decrypted_password = decrypt(server.ssh_password, crypt_key)

        if isinstance(decrypted_password, bytes):
            decrypted_password = decrypted_password.decode()

        ssh_data['ssh_password'] = decrypted_password
        ssh_data['private_key'] = None
    elif ssh_data['ssh_authentication_type'] == 1:
        # retrieve ssh key directory path
        storage_path = get_storage_directory()
        if storage_path:
            # generate full path of ssh key file
            ssh_key_path = os.path.join(
                storage_path,
                server.ssh_key_file.strip('/').strip('\\')
            )
            ssh_data['private_key'] = paramiko.RSAKey.from_private_key_file(ssh_key_path)
            ssh_data['ssh_password'] = None
        else:
            # this will be error
            pass

    return ssh_data
