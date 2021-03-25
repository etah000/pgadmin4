##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2020, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

"""Implements Backup Utility"""

from __future__ import unicode_literals
import simplejson as json
import os

from functools import wraps


from flask import render_template, request, current_app, \
    url_for, Response
from flask_babelex import gettext as _
from flask_security import login_required, current_user
from pgadmin.misc.bgprocess.processes import BatchProcess, IProcessDesc
from pgadmin.utils import PgAdminModule, get_storage_directory, html, \
    fs_short_path, document_dir, does_utility_exist
from pgadmin.utils.ajax import make_json_response, bad_request, internal_server_error
from pgadmin.utils.driver import get_driver

from config import PG_DEFAULT_DRIVER
from pgadmin.model import Server, User, ServerGroup
from pgadmin.misc.bgprocess import escape_dquotes_process_arg
from pgadmin.tools.backup.utils import tempalte_path, create_ir_tables


# set template path for sql scripts
MODULE_NAME = 'backup'
server_info = {}
UTILITY = '/opt/snowball-py3env/bin/python3.7'
PYSCRIPT = '/home/heckler/snowball-py3env/snowball-backup/master.py'


class BackupModule(PgAdminModule):
    """
    class BackupModule(Object):

        It is a utility which inherits PgAdminModule
        class and define methods to load its own
        javascript file.
    """

    LABEL = _('Backup')

    def get_own_javascripts(self):
        """"
        Returns:
            list: js files used by this module
        """
        return [{
            'name': 'pgadmin.tools.backup',
            'path': url_for('backup.index') + 'backup',
            'when': None
        }]

    def show_system_objects(self):
        """
        return system preference objects
        """
        return self.pref_show_system_objects

    def get_exposed_url_endpoints(self):
        """
        Returns:
            list: URL endpoints for backup module
        """
        endpoints = [
            'backup.utility_exists',
            'backup.list_backups',
            'backup.delete_backup',
            'backup.create_backup',
            'backup.restore_backup',
        ]

        return endpoints


# Create blueprint for BackupModule class
blueprint = BackupModule(
    MODULE_NAME, __name__, static_url_path=''
)


class BACKUP(object):
    """
    Constants defined for Backup utilities
    """
    GLOBALS = 1
    SERVER = 2
    OBJECT = 3
    LIST = 4
    DELETE = 5
    CREATE = 6
    RESTORE = 7


class BackupMessage(IProcessDesc):
    """
    BackupMessage(IProcessDesc)

    Defines the message shown for the backup operation.
    """

    def __init__(self, _type, _sid, _bfile, *_args, **_kwargs):
        self.backup_type = _type
        self.sid = _sid
        self.bfile = _bfile
        self.database = _kwargs['database'] if 'database' in _kwargs else None
        self.cmd = ''

        def cmdArg(x):
            if x:
                x = x.replace('\\', '\\\\')
                x = x.replace('"', '\\"')
                x = x.replace('""', '\\"')
                return ' "' + x + '"'
            return ''

        for arg in _args:
            if arg and len(arg) >= 2 and arg[:2] == '--':
                self.cmd += ' ' + arg
            else:
                self.cmd += cmdArg(arg)

    def get_server_details(self):
        # Fetch the server details like hostname, port, roles etc
        s = Server.query.filter_by(
            id=self.sid, user_id=current_user.id
        ).first()

        from pgadmin.utils.driver import get_driver
        driver = get_driver(PG_DEFAULT_DRIVER)
        manager = driver.connection_manager(self.sid)

        host = manager.local_bind_host if manager.use_ssh_tunnel else s.host
        port = manager.local_bind_port if manager.use_ssh_tunnel else s.port

        return s.name, host, port

    def get_server_group_details(self):
        # Fetch the server_group details like id, name etc
        s = Server.query.filter_by(
            id=self.sid, user_id=current_user.id
        ).first()

        g = ServerGroup.query.filter_by(id=s.servergroup_id).first()

        return g.id, g.name

    @property
    def type_desc(self):
        if self.backup_type == BACKUP.OBJECT:
            return _("Backing up an object on the server")
        elif self.backup_type == BACKUP.GLOBALS:
            return _("Backing up the global objects")
        elif self.backup_type == BACKUP.SERVER:
            return _("Backing up the server")
        elif self.backup_type == BACKUP.LIST:
            return _("List backup on group")
        elif self.backup_type == BACKUP.DELETE:
            return _("Delete backup on group")
        elif self.backup_type == BACKUP.CREATE:
            return _("Create backup on group")
        elif self.backup_type == BACKUP.RESTORE:
            return _("Restore backup on group")
        else:
            # It should never reach here.
            return _("Unknown Backup")

    @property
    def message(self):
        name, host, port = self.get_server_details()
        name = html.safe_str(name)
        host = html.safe_str(host)
        port = html.safe_str(port)

        gid, gname = self.get_server_group_details()
        gid = html.safe_str(gid)
        gname = html.safe_str(gname)

        if self.backup_type == BACKUP.OBJECT:
            return _(
                "Backing up an object on the server '{0}' "
                "from database '{1}'"
            ).format(
                "{0} ({1}:{2})".format(
                    name, host, port
                ),
                html.safe_str(self.database)
            )
        if self.backup_type == BACKUP.GLOBALS:
            return _("Backing up the global objects on "
                     "the server '{0}'").format(
                "{0} ({1}:{2})".format(
                    name, host, port
                )
            )
        elif self.backup_type == BACKUP.SERVER:
            return _("Backing up the server '{0}'").format(
                "{0} ({1}:{2})".format(
                    name, host, port
                )
            )
        elif self.backup_type == BACKUP.LIST:
            return _("List backup on group '{0}'").format(
                "{0}".format(gname)
            )
        elif self.backup_type == BACKUP.DELETE:
            return _("Delete  backup on group '{0}'").format(
                "{0}".format(gname)
            )
        elif self.backup_type == BACKUP.CREATE:
            return _("Create  backup on group '{0}'").format(
                "{0}".format(gname)
            )
        elif self.backup_type == BACKUP.RESTORE:
            return _("Restore backup on group '{0}'").format(
                "{0} ".format(gname)
            )
        else:
            # It should never reach here.
            return "Unknown Backup"

    def details(self, cmd, args):
        name, host, port = self.get_server_details()
        gid, gname = self.get_server_group_details()

        res = '<div>'

        if self.backup_type == BACKUP.OBJECT:
            msg = _(
                "Backing up an object on the server '{0}' "
                "from database '{1}'..."
            ).format(
                "{0} ({1}:{2})".format(
                    name, host, port
                ),
                self.database
            )
            res += html.safe_str(msg)
        elif self.backup_type == BACKUP.GLOBALS:
            msg = _("Backing up the global objects on "
                    "the server '{0}'...").format(
                "{0} ({1}:{2})".format(
                    name, host, port
                )
            )
            res += html.safe_str(msg)
        elif self.backup_type == BACKUP.SERVER:
            msg = _("Backing up the server '{0}'...").format(
                "{0} ({1}:{2})".format(
                    name, host, port
                )
            )
            res += html.safe_str(msg)
        elif self.backup_type == BACKUP.LIST:
            msg = _("List backup on group '{0}'...").format(
                "{0} ".format(gname)
            )
            res += html.safe_str(msg)
        elif self.backup_type == BACKUP.DELETE:
            msg = _("Delete backup on group '{0}'...").format(
                "{0} ".format(gname)
            )
            res += html.safe_str(msg)
        elif self.backup_type == BACKUP.CREATE:
            msg = _("Create backup on group '{0}'...").format(
                "{0} ".format(gname)
            )
            res += html.safe_str(msg)
        elif self.backup_type == BACKUP.RESTORE:
            msg = _("Restore backup on group '{0}'...").format(
                "{0} ".format(gname)
            )
            res += html.safe_str(msg)
        else:
            # It should never reach here.
            res += "Backup"

        res += '</div><div class="py-1">'
        res += _("Running command:")
        res += '<div class="pg-bg-cmd enable-selection p-1">'
        res += html.safe_str(cmd + self.cmd)
        res += '</div></div>'

        return res


@blueprint.route("/")
@login_required
def index():
    return bad_request(errormsg=_("This URL cannot be called directly."))


@blueprint.route("/backup.js")
@login_required
def script():
    """render own javascript"""
    return Response(
        response=render_template(
            "backup/js/backup.js", _=_
        ),
        status=200,
        mimetype="application/javascript"
    )


def filename_with_file_manager_path(_file, create_file=True):
    """
    Args:
        file: File name returned from client file manager
        create_file: Set flag to False when file creation doesn't required

    Returns:
        Filename to use for backup with full path taken from preference
    """
    # Set file manager directory from preference
    storage_dir = get_storage_directory()

    if storage_dir:
        _file = os.path.join(storage_dir, _file.lstrip(u'/').lstrip(u'\\'))
    elif not os.path.isabs(_file):
        _file = os.path.join(document_dir(), _file)

    if create_file:
        # Touch the file to get the short path of the file on windows.
        with open(_file, 'a'):
            pass

    short_path = fs_short_path(_file)

    # fs_short_path() function may return empty path on Windows
    # if directory doesn't exists. In that case we strip the last path
    # component and get the short path.
    if os.name == 'nt' and short_path == '':
        base_name = os.path.basename(_file)
        dir_name = os.path.dirname(_file)
        short_path = fs_short_path(dir_name) + '\\' + base_name

    return short_path


def check_precondition(f):
    """
    This function will behave as a decorator which will checks
    connection before running function, it will also attaches
    manager,conn to function kwargs
    """

    @wraps(f)
    def wrap(*args, **kwargs):
        # Here args will hold nothing & kwargs will hold gid

        # snowball-tools must has been installed with pgAdmin on the same host
        if not _check_utility_exists():
            return make_json_response(
                success=0,
                errormsg=_("Could not find the snowball-tools.")
            )

        gid = kwargs.get('gid', None)
        server = Server.query.filter_by(servergroup_id=gid).first()
        sid = server.id if server is not None else None

        if sid is None:
            return make_json_response()

        manager = get_driver(PG_DEFAULT_DRIVER).connection_manager(sid)

        conn = manager.connection()
        already_connected = conn.connected()

        if not already_connected:
            status, errmsg = conn.connect()
            if not status:
                current_app.logger.error(
                    "Could not connected server(#{0}).\nError: {1}"
                    .format(
                        sid, errmsg
                    )
                )
                return internal_server_error(errmsg)
            else:
                current_app.logger.info(
                    'Connection Established for server Id: \
                    %s' % (sid)
                )

        # create maintenance tables in case of not exists
        status, res = create_ir_tables(conn, sync=True)
        if not status:
            return internal_server_error(errormsg=res)

        kwargs['conn'] = conn
        kwargs['mamager'] = manager

        return f(*args, **kwargs)

    return wrap


def _check_utility_exists(*args, **kwargs):
    """
    This function checks the utility file exist on the given path.
    """
    return os.path.exists(UTILITY)


@blueprint.route(
    '/utility_exists/<int:gid>', endpoint='utility_exists'
)
@login_required
def check_utility_exists(gid, ):
    """
    This function checks the utility file exist on the given path.

    Args:
        sid: Server ID
        backup_obj_type: Type of the object
    Returns:
        None
    """
    if _check_utility_exists():
        return make_json_response(success=1)
    else:
        return make_json_response(
            success=0,
            errormsg=_("Could not find the snowball-tools.")
        )


@blueprint.route(
    '/job/<int:gid>', methods=['GET'], endpoint='list_backups'
)
@login_required
@check_precondition
def list_backups(gid, **kwargs):
    """
    Args:
        gid: ServerGroup ID

        Gets backups on ServerGroup: gid
        (Backup Database(s)/Table(s))

    """
    conn = kwargs['conn']

    # retrieve backups
    SQL = render_template(tempalte_path('properties.sql'))
    status, res = conn.execute_dict(SQL)
    if not status:
        return internal_server_error(errormsg=res)

    return make_json_response(data=res['rows'])


@blueprint.route(
    '/job/<int:gid>', methods=['DELETE'], endpoint='delete_backup'
)
@login_required
@check_precondition
def delete_backup(gid, **kwargs):
    """
    Args:
        gid: ServerGroup ID

        Delete a backup on server group 
    """
    # if request.form:
    #     data = json.loads(request.form['data'], encoding='utf-8')
    # else:
    #     data = json.loads(request.data, encoding='utf-8')

    backup_name = request.args.get('backup', '').strip()
    if not backup_name:
        msg = 'required args backup format error'
        return make_json_response(
            status=410,
            success=0,
            errormsg=msg
        )

    args = [
        PYSCRIPT,
        '--config',
        'config.yml',
        'delete',
        backup_name,
    ]

    escaped_args = [
        escape_dquotes_process_arg(arg) for arg in args
    ]

    try:
        p = BatchProcess(
            desc=BackupMessage(
                BACKUP.DELETE,
                gid,
                ''.encode('utf-8'),
                *args
            ),
            cmd=UTILITY, args=escaped_args
        )

        # TODO: after full test, remove the following code
        # manager.export_password_env(p.id)
        # # Check for connection timeout and if it is greater than 0 then
        # # set the environment variable PGCONNECT_TIMEOUT.
        # if manager.connect_timeout > 0:
        #     env = dict()
        #     env['PGCONNECT_TIMEOUT'] = str(manager.connect_timeout)
        #     p.set_env_variables(server, env=env)
        # else:
        #     p.set_env_variables(server)

        p.start()
        jid = p.id
    except Exception as e:
        current_app.logger.exception(e)
        return make_json_response(
            status=410,
            success=0,
            errormsg=str(e)
        )

    # Return response
    return make_json_response(
        data={'job_id': jid, 'Success': 1}
    )


@blueprint.route(
    '/job/<int:gid>', methods=['POST'], endpoint='create_backup'
)
@login_required
@check_precondition
def create_backup(gid, **kwargs):
    """
    Args:
        gid: ServerGroup ID

        Delete a backup on server group 
    """
    if request.form:
        data = json.loads(request.form['data'], encoding='utf-8')
    else:
        data = json.loads(request.data, encoding='utf-8')

    backup_name = data.get('backup', '').strip()
    if not backup_name:
        msg = 'required args backup format error'
        # return gettext('-- definition incomplete')

        return make_json_response(
            status=410,
            success=0,
            errormsg=msg
        )

    args = [
        PYSCRIPT,
        '--config',
        'config.yml',
        'create',
    ]

    def set_param(key, param):
        if key in data and data[key]:
            args.append(param)

    def set_value(key, param, default_value=None):
        if key in data and data[key] is not None and data[key] != '':
            args.append(param)
            args.append(data[key])
        elif default_value is not None:
            args.append(param)
            args.append(default_value)

    set_param('increment', '--increment')
    set_param('schema', '--schema')
    set_value('tables', '--tables')
    set_value('hosts', '--hosts')

    # the last args
    args.append(backup_name)

    escaped_args = [
        escape_dquotes_process_arg(arg) for arg in args
    ]

    try:
        p = BatchProcess(
            desc=BackupMessage(
                BACKUP.CREATE,
                gid,
                ''.encode('utf-8'),
                *args
            ),
            cmd=UTILITY, args=escaped_args
        )

        # TODO: after full test, remove the following code
        # manager.export_password_env(p.id)
        # # Check for connection timeout and if it is greater than 0 then
        # # set the environment variable PGCONNECT_TIMEOUT.
        # if manager.connect_timeout > 0:
        #     env = dict()
        #     env['PGCONNECT_TIMEOUT'] = str(manager.connect_timeout)
        #     p.set_env_variables(server, env=env)
        # else:
        #     p.set_env_variables(server)

        p.start()
        jid = p.id
    except Exception as e:
        current_app.logger.exception(e)
        return make_json_response(
            status=410,
            success=0,
            errormsg=str(e)
        )

    # Return response
    return make_json_response(
        data={'job_id': jid, 'Success': 1}
    )


@blueprint.route(
    '/job/<int:gid>', methods=['PUT'], endpoint='restore_backup'
)
@login_required
@check_precondition
def restore_backup(gid, **kwargs):
    """
    Args:
        gid: ServerGroup ID

        Delete a backup on server group 
    """
    if request.form:
        data = json.loads(request.form['data'], encoding='utf-8')
    else:
        data = json.loads(request.data, encoding='utf-8')

    backup_name = data.get('backup', '').strip()
    if not backup_name:
        msg = 'required args backup format error'
        # return gettext('-- definition incomplete')

        return make_json_response(
            status=410,
            success=0,
            errormsg=msg
        )

    args = [
        PYSCRIPT,
        '--config',
        'config.yml',
        'restore',
    ]

    def set_param(key, param):
        if key in data and data[key]:
            args.append(param)

    def set_value(key, param, default_value=None):
        if key in data and data[key] is not None and data[key] != '':
            args.append(param)
            args.append(data[key])
        elif default_value is not None:
            args.append(param)
            args.append(default_value)

    set_param('data', '--data')
    set_param('schema', '--schema')
    set_param('attach', '--attach')
    set_value('tables', '--tables')
    set_value('hosts', '--hosts')

    # the last args
    args.append(backup_name)

    escaped_args = [
        escape_dquotes_process_arg(arg) for arg in args
    ]

    try:
        p = BatchProcess(
            desc=BackupMessage(
                BACKUP.RESTORE,
                gid,
                ''.encode('utf-8'),
                *args
            ),
            cmd=UTILITY, args=escaped_args
        )

        # TODO: after full test, remove the following code
        # manager.export_password_env(p.id)
        # # Check for connection timeout and if it is greater than 0 then
        # # set the environment variable PGCONNECT_TIMEOUT.
        # if manager.connect_timeout > 0:
        #     env = dict()
        #     env['PGCONNECT_TIMEOUT'] = str(manager.connect_timeout)
        #     p.set_env_variables(server, env=env)
        # else:
        #     p.set_env_variables(server)

        p.start()
        jid = p.id
    except Exception as e:
        current_app.logger.exception(e)
        return make_json_response(
            status=410,
            success=0,
            errormsg=str(e)
        )

    # Return response
    return make_json_response(
        data={'job_id': jid, 'Success': 1}
    )
