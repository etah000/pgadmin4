##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2020, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

"""Database helper utilities"""


from flask_babelex import gettext


from pgadmin.browser.utils import PGChildNodeView
from pgadmin.model import Server
from config import PG_DEFAULT_DRIVER
from pgadmin.utils.ajax import make_json_response, precondition_required,\
    internal_server_error
from pgadmin.utils.exception import ConnectionLost, SSHTunnelConnectionLost,\
    CryptKeyMissing


def parse_sec_labels_from_db(db_sec_labels):
    """
    Function to format the output for security label.

    Args:
        db_sec_labels : Security Label Array in (provider=label) format

    Returns:
        Security Label Object in below format:
            {'seclabels': [{'provider': 'provider_name', 'label':
            'label'},...]}
    """
    sec_lbls = []

    if db_sec_labels is not None:
        for sec in db_sec_labels:
            import re
            sec = re.search(r'([^=]+)=(.*$)', sec)
            sec_lbls.append({
                'provider': sec.group(1),
                'label': sec.group(2)
            })

    return {"seclabels": sec_lbls}


def parse_variables_from_db(db_variables):
    """
    Function to format the output for variables.

    Args:
        db_variables: Variable object

            Expected Object Format:
                [
                    {
                    'setconfig': Variable Config Parameters,
                    'user_name': User Name,
                    'db_name': Database Name
                    },...
                ]
            where:
                user_name and database are optional
    Returns:
        Variable Object in below format:
            {
            'variables': [
                {'name': 'var_name', 'value': 'var_value',
                'user_name': 'user_name', 'database': 'database_name'},
                ...]
            }
            where:
                user_name and database are optional
    """
    variables_lst = []

    if db_variables is not None:
        for row in db_variables:
            if 'setconfig' in row and row['setconfig'] is not None:
                for d in row['setconfig']:
                    var_name, var_value = d.split("=")
                    # Because we save as boolean string in db so it needs
                    # conversion
                    if var_value == 'false' or var_value == 'off':
                        var_value = False

                    var_dict = {
                        'name': var_name,
                        'value': var_value
                    }
                    if 'user_name' in row:
                        var_dict['role'] = row['user_name']
                    if 'db_name' in row:
                        var_dict['database'] = row['db_name']

                    variables_lst.append(var_dict)

    return {"variables": variables_lst}



class PGClusterChildNodeView(PGChildNodeView):

    def children(self, **kwargs):
        """Build a list of treeview nodes from the child nodes."""

        sid = kwargs.get('sid', None)
        if sid is None:
            gid = kwargs['gid']
            server = Server.query.filter_by(servergroup_id=gid).first()
            sid = server.id if server is not None else None
            kwargs['sid'] = sid

        if sid is None:
            return make_json_response()

        from pgadmin.utils.driver import get_driver
        manager = get_driver(PG_DEFAULT_DRIVER).connection_manager(
            sid=kwargs['sid']
        )

        try:
            conn = manager.connection()
            if not conn.connected():
                status, msg = conn.connect()
                if not status:
                    return internal_server_error(errormsg=msg)
        except (ConnectionLost, SSHTunnelConnectionLost, CryptKeyMissing):
            raise
        except Exception as e:
            return precondition_required(
                gettext(
                    "Connection to the server has been lost."
                )
            )

        # Return sorted nodes based on label
        return make_json_response(
            data=sorted(
                self.get_children_nodes(manager, **kwargs),
                key=lambda c: c['label']
            )
        )
