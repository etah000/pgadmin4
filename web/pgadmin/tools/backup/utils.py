##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2020, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

"""Backup helper utilities"""

import os
import socket

from flask import current_app, render_template
from flask_babelex import gettext as _


from pgadmin.model import Server
from pgadmin.utils.ajax import make_json_response, internal_server_error, gone
from pgadmin.utils.driver import get_driver


from config import PG_DEFAULT_DRIVER


def tempalte_path(sql_template):
    return os.path.join('backup/sql/default', sql_template)


def create_ir_tables(conn, sync=True):
    """create inforefiner database and related tables for maintenance(backup&restore).

    database:
        ir

    tables:
        backup
        part
        etc
        metadata
    """

    SQL = render_template(tempalte_path('check_db_ir.sql'))
    status, res = conn.execute_dict(SQL)
    if not status:
        return status, res

    if len(res['rows']) != 4:
        hostname = conn.manager.host

        # CREATE DATABASE IF NOT EXISTS ir;
        SQL = render_template(tempalte_path('create_db_ir.sql'),
                              hostname=hostname, )
        status, res = conn.execute_void(SQL)
        if not status:
            return status, res

        # CREATE TABLE IF NOT EXISTS ir.backup;
        SQL = render_template(tempalte_path('create_table_ir_backup.sql'),
                              hostname=hostname, )
        status, res = conn.execute_void(SQL)
        if not status:
            return status, res

        # CREATE TABLE IF NOT EXISTS ir.part;
        SQL = render_template(tempalte_path('create_table_ir_part.sql'),
                              hostname=hostname, )
        status, res = conn.execute_void(SQL)
        if not status:
            return status, res

        # CREATE TABLE IF NOT EXISTS ir.etc;
        SQL = render_template(tempalte_path('create_table_ir_etc.sql'),
                              hostname=hostname, )
        status, res = conn.execute_void(SQL)
        if not status:
            return status, res

        # CREATE TABLE IF NOT EXISTS ir.metadata;
        SQL = render_template(tempalte_path('create_table_ir_metadata.sql'),
                              hostname=hostname, )
        status, res = conn.execute_void(SQL)
        if not status:
            return status, res

    if sync:
        status, res = conn.execute_void('SYSTEM SYNC REPLICA ir.backup')
        if not status:
            return status, res

        status, res = conn.execute_void('SYSTEM SYNC REPLICA ir.part')
        if not status:
            return status, res

        status, res = conn.execute_void('SYSTEM SYNC REPLICA ir.etc')
        if not status:
            return status, res

        status, res = conn.execute_void('SYSTEM SYNC REPLICA ir.metadata')
        if not status:
            return status, res

    return True, None
