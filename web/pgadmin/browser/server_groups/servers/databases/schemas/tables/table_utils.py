"""Create shift-replicated tables.

Features:

1. create shift-replicated tables using MergeTree or ReplicatedMergeTree;
2. create distributed tables in standalone database of not;
"""


import sys
import os
import re
import argparse
import logging

from collections import defaultdict

DIST_SQL = (
    """CREATE TABLE IF NOT EXISTS {dist_db}.{dist_table} """
    """AS {local_db}.{local_table} """
    """ENGINE = Distributed({cluster}, '', {local_table}, rand());"""
)


class _Server(object):
    """represents a physical server
    """

    def __init__(self, conn):
        """

        :param conn: 
        :type conn: a wrapped Connection instance

        """
        self.conn = conn

    def execute(self, stmt, ):
        try:
            status, result = self.conn.execute_dict(stmt)
            return status, result
        except Exception as ex:
            return False, str(ex)

    def get_rmt_database(self, cluster):
        """select default_database who's replica_num == 1
        """
        stmt = """
            SELECT default_database
            FROM system.clusters
            WHERE (cluster = '{cluster}') AND (replica_num = 1)
            LIMIT 1
        """.format(cluster=cluster)

        status, result = self.execute(stmt)

        rmt_database = result['rows'][0]['default_database']

        return rmt_database

    def get_replicas(self, cluster):
        """make Replica objects from system.clusters
        """
        stmt = """
            SELECT *
            FROM system.clusters
            WHERE (host_name NOT LIKE 'localhost') 
                AND (host_name NOT LIKE '127.0.0.%') 
                AND (cluster = '{cluster}')
        """.format(cluster=cluster)

        status, result = self.execute(stmt)

        replicas = [Replica(self.conn, info) for info in result['rows']]

        return replicas

    def get_default_databases(self, cluster):
        stmt = """
            SELECT DISTINCT default_database
            FROM system.clusters
            WHERE (host_name NOT LIKE 'localhost') 
                AND (host_name NOT LIKE '127.0.0.%') 
                AND (cluster = '{cluster}')
        """.format(cluster=cluster)

        status, result = self.execute(stmt)

        default_databases = [info['default_database'] for info in result['rows']]

        return default_databases


class Replica(_Server):
    """represents any replication
    """

    def __init__(self, conn, replica_info):
        super(Replica, self).__init__(conn)

        self.info = replica_info

        for attr, value in replica_info.items():
            setattr(self, attr, value)

    def _renew_conn(self, ):
        manager = self.conn.manager.copy(
            host=self.host_name, hostaddr=self.host_address, )

        conn = manager.connection()
        connected = conn.connected()
        if not conn.connected():
            conn.connect()

        self.conn = conn

    def create_database(self, database):
        """
        """
        stmt = 'CREATE DATABASE IF NOT EXISTS {};'.format(database)
        return self.execute(stmt)

    def create_table(self, ddl):
        """
        """
        return self.execute(ddl)


def shifter(conn, cluster, tbl_ddl_template=None, tbl_name=None,
            dist_db=None, dist_tbl_suffix=None, local_tbl_suffix=None):

    ch = _Server(conn)
    replicas = ch.get_replicas(cluster)
    rmt_db = ch.get_rmt_database(cluster)
    default_dbs = ch.get_default_databases(cluster)

    if dist_db in default_dbs and dist_tbl_suffix == local_tbl_suffix:
        dist_tbl_suffix = None
        local_tbl_suffix = 'local'

    local_table = tbl_name + '_' + local_tbl_suffix if local_tbl_suffix else tbl_name
    dist_table = tbl_name + '_' + dist_tbl_suffix if dist_tbl_suffix else tbl_name
    SQL = tbl_ddl_template

    rsp = defaultdict(lambda: defaultdict(dict))
    # rsp = {
    #     'replica_id: {
    #         'db': {
    #             'success': True,
    #             'errormsg': None,
    #         },
    #         'db.tbl': {
    #             'success': True,
    #             'errormsg': None,
    #         },
    #     },
    # }

    for replica in replicas:
        replica_id = '{}_{}'.format(replica.shard_num, replica.replica_num)
        replica._renew_conn()

        # 1. create replication database
        db = replica.default_database
        status, rst = replica.create_database(db)
        rsp[replica_id][db]['success'] = status
        rsp[replica_id][db]['errormsg'] = (not status and rst)

        # 2. create replication local table
        fullname = '{}.{}'.format(db, local_table)
        ddl = SQL.format(
            database=db,
            local_table=local_table,
            rmt_db=rmt_db,
            shard_num=replica.shard_num,
            replica_num=replica.replica_num,
        )

        status, rst = replica.create_table(ddl)
        rsp[replica_id][fullname]['success'] = status
        rsp[replica_id][fullname]['errormsg'] = (not status and rst)

        # set default distributed database
        if not dist_db:
            db = replica.default_database
        elif dist_db and replica.replica_num == 1:
            db = dist_db
        else:
            continue

        # 3. create distributed database
        status, rst = replica.create_database(db)
        rsp[replica_id][db]['success'] = status
        rsp[replica_id][db]['errormsg'] = (not status and rst)

        # 4. create distributed table
        dist_fullname = '{}.{}'.format(db, dist_table)
        dist_ddl = DIST_SQL.format(
            dist_db=db,
            dist_table=dist_table,
            local_db=replica.default_database,
            local_table=local_table,
            cluster=cluster,
        )

        status, rst = replica.create_table(dist_ddl)
        rsp[replica_id][dist_fullname]['success'] = status
        rsp[replica_id][dist_fullname]['errormsg'] = (not status and rst)

    return rsp
