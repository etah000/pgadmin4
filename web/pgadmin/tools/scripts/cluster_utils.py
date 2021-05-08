# -*- coding: utf-8 -*-

"""Generate remote_servers definition xml

This will be a module of pgAdmin.
"""
from collections import defaultdict
from operator import itemgetter


from lxml import etree as ET


def check_xml(xml_str):
    status = None

    try:
        rst = ET.fromstring(xml_str)
        status = True
    except Exception as e:
        rst = str(e)

    return status, rst


class Cluster(object):
    def __init__(self, cluster, hosts, ports=None, default_databases=None, shifted=None):
        self.cluster = cluster
        self.hosts = hosts
        self.ports = ports
        self.default_databases = default_databases
        self.shifted = shifted

        self.etree = None
        self._create_cluster()

    def _create_cluster(self, ):
        self.etree = ET.Element(self.cluster)

        n_replica = 1
        if self.shifted and self.default_databases:
            n_replica = len(self.default_databases)

        replica_hosts = [
            self.hosts[i:] + self.hosts[:i]
            for i in range(n_replica)
        ]
        shard_hosts = list(zip(*replica_hosts))

        for shard_host in shard_hosts:
            shard = self._get_shard(shard_host)
            self.etree.append(shard)

    def _get_shard(self, shard_host):
        shard = ET.Element('shard')
        internal_replication = ET.SubElement(shard, 'internal_replication')
        internal_replication.text = 'true'

        for idx, host in enumerate(shard_host):
            replica = self._get_replica(idx, host)
            shard.append(replica)

        return shard

    def _get_replica(self, idx, host):
        replica = ET.Element('replica')

        if self.shifted:
            default_database = ET.SubElement(replica, 'default_database')
            default_database.text = self.default_databases[idx]
        elif self.default_databases:
            default_database = ET.SubElement(replica, 'default_database')
            default_database.text = self.default_databases[0]

        et_host = ET.SubElement(replica, 'host')
        et_host.text = host

        # TODO: add supports to run multi DB instances on single host
        # that is instances has different ports
        et_port = ET.SubElement(replica, 'port')
        et_port.text = '9000'

        return replica

    def to_str(self, ):
        yandex = ET.Element('yandex')
        remote_servers = ET.SubElement(yandex, 'remote_servers')
        remote_servers.append(self.etree)

        xml_str = ET.tostring(yandex,
                              encoding='UTF-8',
                              xml_declaration=True,
                              pretty_print=True, )
        xml_str = xml_str.decode()

        return xml_str


class ClusterUpdater(object):
    def __init__(self, cluster, data, ):
        self.cluster = cluster
        self.data = data

        self.etree = None
        self._create_cluster()

    def _create_cluster(self, ):
        self.etree = ET.Element(self.cluster)

        cate_data = defaultdict(list)

        for replica in self.data:
            shard_num = replica.get('shard_num')
            replica_num = replica.get('replica_num')
            cate_data[shard_num].append(replica)

        for shard_num in sorted(cate_data):
            shard_info = cate_data[shard_num]
            shard = self._get_shard(shard_info)
            self.etree.append(shard)

    def _get_shard(self, shard_info):
        shard = ET.Element('shard')

        internal_replication = ET.SubElement(shard, 'internal_replication')
        internal_replication.text = 'true'

        for replica_info in sorted(shard_info, key=itemgetter('replica_num')):
            replica = self._get_replica(replica_info)
            shard.append(replica)

        return shard

    def _get_replica(self, replica_info):
        replica = ET.Element('replica')

        default_database = ET.SubElement(replica, 'default_database')
        default_database.text = replica_info['default_database']

        et_host = ET.SubElement(replica, 'host')
        et_host.text = replica_info['host_name']

        et_port = ET.SubElement(replica, 'port')
        et_port.text = str(replica_info['port'])

        return replica

    def to_str(self, ):
        yandex = ET.Element('yandex')
        remote_servers = ET.SubElement(yandex, 'remote_servers')
        remote_servers.append(self.etree)

        xml_str = ET.tostring(yandex,
                              encoding='UTF-8',
                              xml_declaration=True,
                              pretty_print=True, )
        xml_str = xml_str.decode()

        return xml_str


if __name__ == '__main__':
    # shifted_cluster
    cluster = Cluster('shifted_cluster',
                      hosts=('c1', 'c2', 'c3'),
                      default_databases=('db_r1', 'db_r2'),
                      shifted=True)

    print(cluster.to_str())

    # normal cluster with default_database
    cluster = Cluster('shifted_cluster',
                      hosts=('c1', 'c2', 'c3'),
                      default_databases=('db_r1', ),
                      shifted=False)

    print(cluster.to_str())

    # normal cluster without default_database
    cluster = Cluster('shifted_cluster',
                      hosts=('c1', 'c2', 'c3'),
                      default_databases=None,
                      shifted=False)

    print(cluster.to_str())
