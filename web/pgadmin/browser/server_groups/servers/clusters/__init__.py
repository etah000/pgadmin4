##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2020, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

"""Implements the Database Node"""

import io
import os
import re
from functools import wraps

import simplejson as json
from flask import render_template, current_app, request, jsonify, Response
from flask_babelex import gettext as _
from flask_security import current_user

import pgadmin.browser.server_groups.servers as servers
from config import PG_DEFAULT_DRIVER
from pgadmin.browser.collection import CollectionNodeModule
from pgadmin.browser.server_groups.servers.databases.utils import \
    parse_sec_labels_from_db, parse_variables_from_db
from pgadmin.browser.server_groups.servers.utils import parse_priv_from_db, \
    parse_priv_to_db
from pgadmin.browser.utils import PGChildNodeView
from pgadmin.browser.server_groups.servers.clusters.utils import PGClusterChildNodeView
from pgadmin.utils.ajax import gone
from pgadmin.utils.ajax import make_json_response, \
    make_response as ajax_response, internal_server_error, unauthorized
from pgadmin.utils.driver import get_driver
from pgadmin.tools.sqleditor.utils.query_history import QueryHistory

from pgadmin.tools.schema_diff.node_registry import SchemaDiffRegistry
from pgadmin.model import Server, ServerGroup
from pgadmin.browser.server_groups.servers.utils import get_ssh_client, get_ssh_info
from pgadmin.tools.scripts.cluster_utils import check_xml, ClusterUpdater


class DatabaseModule(CollectionNodeModule):
    NODE_TYPE = 'cluster'
    COLLECTION_LABEL = _("Virtual Clusters")

    def __init__(self, *args, **kwargs):
        self.min_ver = None
        self.max_ver = None

        super(DatabaseModule, self).__init__(*args, **kwargs)

    def get_nodes(self, gid, sid):
        """
        Generate the collection node
        """
        if self.show_node:
            yield self.generate_browser_collection_node(sid)

    @property
    def script_load(self):
        """
        Load the module script for server, when any of the server-group node is
        initialized.
        """
        return servers.ServerModule.NODE_TYPE

    @property
    def csssnippets(self):
        """
        Returns a snippet of css to include in the page
        """
        snippets = [
            render_template(
                "browser/css/collection.css",
                node_type=self.node_type,
                _=_
            ),
            render_template(
                "databases/css/database.css",
                node_type=self.node_type,
                _=_
            )
        ]

        for submodule in self.submodules:
            snippets.extend(submodule.csssnippets)

        return snippets

    @property
    def module_use_template_javascript(self):
        """
        Returns whether Jinja2 template is used for generating the javascript
        module.
        """
        return False


blueprint = DatabaseModule(__name__)


class DatabaseView(PGClusterChildNodeView):
    node_type = blueprint.node_type

    parent_ids = [
        {'type': 'int', 'id': 'gid'},
        # {'type': 'int', 'id': 'sid'},
    ]
    ids = [
        # {'type': 'int', 'id': 'sid'},
        {'type': 'string', 'id': 'did'}
    ]

    operations = dict({
        'obj': [
            {'get': 'properties', 'delete': 'delete', 'put': 'update'},
            {'get': 'list', 'post': 'create', 'delete': 'delete'}
        ],
        'nodes': [
            {'get': 'node'},
            {'get': 'nodes'}
        ],
        # 'get_databases': [
        #     {'get': 'get_databases'},
        #     {'get': 'get_databases'}
        # ],
        # 'sql': [
        #     {'get': 'sql'}
        # ],
        # 'msql': [
        #     {'get': 'msql'},
        #     {'get': 'msql'}
        # ],
        # 'stats': [
        #     {'get': 'statistics'},
        #     {'get': 'statistics'}
        # ],
        # 'dependency': [
        #     {'get': 'dependencies'}
        # ],
        # 'dependent': [
        #     {'get': 'dependents'}
        # ],
        'children': [
            {'get': 'children'}
        ],
        'connect': [
            {
                'get': 'connect_status',
                'post': 'connect',
                'delete': 'disconnect'
            }
        ],
        # 'get_encodings': [
        #     {'get': 'get_encodings'},
        #     {'get': 'get_encodings'}
        # ],
        # 'get_ctypes': [
        #     {'get': 'get_ctypes'},
        #     {'get': 'get_ctypes'}
        # ],
        # 'vopts': [
        #     {}, {'get': 'variable_options'}
        # ],
        'get_hosts': [
            {'get': 'get_hosts'},
            {'get': 'get_hosts'}
        ],
    })

    def check_precondition(action=None):
        """
        This function will behave as a decorator which will checks
        database connection before running view, it will also attaches
        manager,conn & template_path properties to self
        """

        def wrap(f):
            @wraps(f)
            def wrapped(self, *args, **kwargs):
                sid = kwargs.get('sid', None)
                if sid is None:
                    gid = kwargs['gid']
                    server = Server.query.filter_by(servergroup_id=gid).first()
                    sid = server.id if server is not None else None
                    kwargs['sid'] = sid

                if sid is None:
                    return make_json_response()

                self.manager = get_driver(
                    PG_DEFAULT_DRIVER
                ).connection_manager(
                    kwargs['sid']
                )
                if self.manager is None:
                    return gone(errormsg=_("Could not find the server."))

                self.datlastsysoid = 0
                self.conn = self.manager.connection()

                conn = self.conn
                already_connected = conn.connected()
                if not already_connected:
                    status, errmsg = conn.connect()
                    if not status:
                        current_app.logger.error("Could not connected server(#{0}).\nError: {1}"
                            .format(
                                sid, errmsg
                            )
                        )
                        msg = _("Could not connected server(#{0}).\nError: {1}").format(
                                sid, errmsg
                            )
                        return internal_server_error(msg)
                    else:
                        current_app.logger.info(
                            'Connection Established for server Id: \
                            %s' % (sid)
                        )

                # set template path for sql scripts
                self.template_path = 'clusters/sql/#{0}#'.format(
                    self.manager.version
                )

                return f(self, *args, **kwargs)

            return wrapped

        return wrap

    @check_precondition(action="list")
    def list(self, gid, sid):
        SQL = render_template(
            "/".join([self.template_path, 'properties.sql']),
            conn=self.conn,
        )
        status, res = self.conn.execute_dict(SQL, )

        if not status:
            return internal_server_error(errormsg=res)

        return ajax_response(
            response=res['rows'],
            status=200
        )

    def get_nodes(self, gid, sid, did=None):
        res = []
        SQL = render_template(
            "/".join([self.template_path, 'nodes.sql']),
            did=did,
        )
        status, rset = self.conn.execute_dict(SQL, )

        if not status:
            return internal_server_error(errormsg=rset)

        for row in rset['rows']:
            res.append(
                self.blueprint.generate_browser_node(
                    row['did'],
                    sid,
                    row['name'],
                    icon="pg-icon-database",
                    connected=False,
                    tablespace=row['spcname'],
                    allowConn=True,
                    canCreate=True,
                    canDisconn=True,
                    canDrop=True,
                    inode=True,
                )
            )

        return res

    @check_precondition(action="nodes")
    def nodes(self, gid, sid):
        res = self.get_nodes(gid, sid)

        if isinstance(res, Response):
            return res

        return make_json_response(
            data=res,
            status=200
        )

    @check_precondition(action="node")
    def node(self, gid, sid, did):
        res = self.get_nodes(gid, sid, did)

        if isinstance(res, Response):
            return res

        if len(res) == 0:
            return gone(errormsg=_("Could not find the cluster on the server."))

        return make_json_response(
            data=res[0],
            status=200
        )

    @check_precondition(action="properties")
    def properties(self, gid, sid, did):

        SQL = render_template(
            "/".join([self.template_path, 'properties.sql']),
            did=did,
            conn=self.conn,
        )
        status, res = self.conn.execute_dict(SQL)

        if not status:
            return internal_server_error(errormsg=res)

        if len(res['rows']) == 0:
            return gone(
                _("Could not find the virtual cluster on the server.")
            )

        return ajax_response(
            response=res['rows'],
            status=200
        )

    @check_precondition(action="connect")
    def connect(self, gid, sid, did):
        """Connect the Database."""

        return make_json_response(
            success=1,
            info=_("Database connected."),
            data={
                'icon': 'pg-icon-database',
                'already_connected': True,
                'connected': True,
                'info_prefix': '{0}/{1}'.
                format(Server.query.filter_by(id=sid)[0].name, did)
            }
        )

    def disconnect(self, gid, sid, did):
        """Disconnect the database."""
        return make_json_response(
            success=1,
            info=_("Database disconnected."),
            data={
                'icon': 'icon-database-not-connected',
                'connected': False,
                'info_prefix': '{0}/{1}'.
                format(Server.query.filter_by(id=sid)[0].name, did)
            }
        )

    # @check_precondition(action="get_encodings")
    # def get_encodings(self, gid, sid, did=None):
    #     """
    #     This function to return list of avialable encodings
    #     """
    #     res = [{'label': 'UTF8', 'value': 'UTF8'}]

    #     return make_json_response(
    #         data=res,
    #         status=200
    #     )

    # @check_precondition(action="get_ctypes")
    # def get_ctypes(self, gid, sid, did=None):
    #     """
    #     This function to return list of available collation/character types
    #     """
    #     res = [{'label': '', 'value': ''}]

    #     return make_json_response(
    #         data=res,
    #         status=200
    #     )

    @check_precondition(action="create")
    def create(self, gid, sid):
        """Create the database."""
        required_args = [
            u'name',
            u'hosts',
            u'data',
        ]

        data = request.form if request.form else json.loads(
            request.data, encoding='utf-8'
        )

        for arg in required_args:
            if arg not in data:
                return make_json_response(
                    status=410,
                    success=0,
                    errormsg=_(
                        "Could not find the required parameter ({})."
                    ).format(arg)
                )

        # check xml_str
        status, msg = check_xml(data['data'])
        if not status:
            return make_json_response(
                status=410,
                success=0,
                errormsg=_("XMLSyntaxError ({}).").format(msg)
            )

        did = data['name']

        # make sure cluster does not exists
        SQL = render_template(
            "/".join([self.template_path, 'get_hosts.sql']),
            did=did, conn=self.conn,
        )
        status, rset = self.conn.execute_2darray(SQL)

        if not status:
            return internal_server_error(errormsg=rset)

        if rset['rows']:
            errmsg = _('cluster: {} existed.'.format(data['name']))
            return make_json_response(
                success=0,
                errormsg=errmsg
            )

        status, msg = self.write_remote_file(gid, sid, did, data['data'])
        if not status:
            return make_json_response(
                success=0,
                errormsg=msg
            )

        return jsonify(
            node=self.blueprint.generate_browser_node(
                data['name'],
                gid,
                data['name'],
                icon="pg-icon-database",
                connected=False,
                tablespace='public',
                allowConn=True,
                canCreate=True,
                canDisconn=True,
                canDrop=True
            )
        )

    def get_ssh_infos(self, gid, sid=None):
        """Update the database.

        Args:
            gid: ServerGroup id
            sid: Server id
        """
        sg = ServerGroup.query.filter_by(id=gid).first()
        servers = Server.query.filter_by(servergroup_id=gid).all()

        # get ssh connection info and check
        ssh_infos = dict()
        ssh_null_servers = list()
        for server in servers:
            ssh_info = get_ssh_info(gid, server.id)
            if not ssh_info:
                ssh_null_servers.append(server)

            ssh_infos[server.id] = ssh_info

        if ssh_null_servers:
            server_names = ['{}.{}'.format(sg.name, server.name) for server in ssh_null_servers]
            errmsg = _('please submit ssh connection information in properties for server: {}'
                       .format(','.join(server_names)))
            return None, errmsg

        return True, ssh_infos

    def write_remote_file(self, gid, sid, did, data):
        """Update the database.

        Args:
            gid: ServerGroup id
            sid: Server id
            did: Cluster id
            data: xml str
        """
        sg = ServerGroup.query.filter_by(id=gid).first()
        servers = Server.query.filter_by(servergroup_id=gid).all()

        # get ssh connection info and check
        ssh_infos = dict()
        ssh_null_servers = list()
        for server in servers:
            ssh_info = get_ssh_info(gid, server.id)
            if not ssh_info:
                ssh_null_servers.append(server)

            ssh_infos[server.id] = ssh_info

        if ssh_null_servers:
            server_names = [server.name for server in ssh_null_servers]
            errmsg = _('please submit ssh connection information in properties for server: {}'
                       .format(','.join(server_names)))
            return None, errmsg

        fl = io.StringIO(data)

        remote_path = os.path.join('/etc/snowball-server/config.d', '{}.xml'.format(did))

        created_servers = list()
        for server in servers:
            try:
                ssh_client = get_ssh_client(server.host,
                                            user=ssh_info['ssh_username'],
                                            port=ssh_info['ssh_port'],
                                            password=ssh_info['ssh_password'],
                                            pkey=ssh_info['private_key'],)

                fl.seek(0, os.SEEK_SET)
                ssh_client.execute_cmd('mkdir -p /etc/snowball-server/config.d')
                ssh_client.putfo(fl, remote_path)
                ssh_client.disconnect()

                created_servers.append(server)
            except Exception as ex:
                try:
                    self.delete_remote_file(gid, sid, did)
                except Exception:
                    pass

                errmsg = _('server error: {}, {}'.format(server.name, ex))
                return None, errmsg

        return True, None

    def delete_remote_file(self, gid, sid, did, ignore_error=True):
        """Update the database.

        Args:
            gid: ServerGroup id
            sid: Server id
            did: Cluster id
        """
        sg = ServerGroup.query.filter_by(id=gid).first()
        servers = Server.query.filter_by(servergroup_id=gid).all()

        # get ssh connection info and check
        ssh_infos = dict()
        ssh_null_servers = list()
        for server in servers:
            ssh_info = get_ssh_info(gid, server.id)
            if not ssh_info:
                ssh_null_servers.append(server)

            ssh_infos[server.id] = ssh_info

        if ssh_null_servers:
            server_names = ['{}.{}'.format(sg.name, server.name) for server in ssh_null_servers]
            errmsg = _('please submit ssh connection information in properties for server: {}'
                       .format(','.join(server_names)))
            return None, errmsg

        remote_path = os.path.join('/etc/snowball-server/config.d', '{}.xml'.format(did))

        deleted_servers = list()
        for server in servers:
            try:
                ssh_client = get_ssh_client(server.host,
                                            user=ssh_info['ssh_username'],
                                            port=ssh_info['ssh_port'],
                                            password=ssh_info['ssh_password'],
                                            pkey=ssh_info['private_key'],)

                ssh_client.execute_cmd('rm -f {}'.format(remote_path))
                ssh_client.disconnect()

                deleted_servers.append(server)
            except Exception as ex:
                if not ignore_error:
                    errmsg = _('server error: {}, {}'.format(server.name, ex))
                    return None, errmsg

        return True, None

    @check_precondition(action='update')
    def update(self, gid, sid, did):
        """Update the database."""

        data = request.form if request.form else json.loads(
            request.data, encoding='utf-8'
        )

        # make sure cluster already existed
        SQL = render_template(
            "/".join([self.template_path, 'get_hosts.sql']),
            did=did, conn=self.conn,
        )
        status, rset = self.conn.execute_2darray(SQL)

        if not status:
            return internal_server_error(errormsg=rset)

        if not rset['rows']:
            errmsg = _('Could not find the required cluster.')
            return make_json_response(
                status=410,
                success=0,
                errormsg=errmsg
            )

        cluster_str = ClusterUpdater(did, data).to_str()

        status, errmsg = self.write_remote_file(gid, sid, did, cluster_str)
        if not status:
            return make_json_response(
                success=0,
                errormsg=errmsg
            )

        return jsonify(
            node=self.blueprint.generate_browser_node(
                did,
                gid,
                did,
                icon="pg-icon-database",
                connected=False,
                tablespace='public',
                allowConn=True,
                canCreate=True,
                canDisconn=True,
                canDrop=True,
                inode=True
            )
        )

    @check_precondition(action="drop")
    def delete(self, gid, sid, did=None):
        """Delete the cluster configuration file via ssh on physical cluster."""

        if did is None:
            data = request.form if request.form else json.loads(
                request.data, encoding='utf-8'
            )

            if not data['ids']:
                return make_json_response(success=1)
            else:
                did = data['ids'][0]

        status, errmsg = self.delete_remote_file(gid, sid, did, ignore_error=False)
        if not status:
            return make_json_response(
                success=0,
                errormsg=errmsg,
            )

        return make_json_response(
            success=1,
            info=_('Cluster deleted')
        )

    @check_precondition(action="get_hosts")
    def get_hosts(self, gid, sid, did=None):
        """
        This function get host and port within the ServerGroup.

        Args:
            gid: Server Group ID
            sid: Server ID
            did: Database ID
        """

        servers = Server.query.filter_by(servergroup_id=gid).all()
        hosts = [{'host_name': s.host, 'port': s.port} for s in servers]

        return make_json_response(data=hosts, status=200)

    def get_server_group_hosts(self, gid, ):
        """
        This function get hosts within the ServerGroup.

        Args:
            gid: Server Group ID
        """
        servers = Server.query.filter_by(servergroup_id=gid).all()
        hosts = [s.host for s in servers]

        return hosts


SchemaDiffRegistry(blueprint.node_type, DatabaseView)
DatabaseView.register_node_view(blueprint)
