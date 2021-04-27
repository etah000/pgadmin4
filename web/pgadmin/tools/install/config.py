# coding: utf-8

import configparser
import xmltodict
from pgadmin.tools.install.installer.common import GetSelfPath
# import json
selfPath = GetSelfPath()
# 修改为区分大小写
class MyConfigParser(configparser.ConfigParser):

    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr


class AbstractConfig():

    def __init__(self, confile):
        # self.parser = ConfigParser.ConfigParser()
        self.parser = MyConfigParser()
        self.parser.read(confile)

    def has_option(self,namespaces,option):
        return  self.parser.has_option(namespaces,option)

    def has_section(self,option):
        return  self.parser.has_section(option)

    def get(self, namespaces, key):
        info = self.parser.get(namespaces, key)
        return info;

    def items(self, namespaces):
        # if self.parser.has_section(namespaces):
        return self.parser.items(namespaces)
        # else :
        #     return  []
        # return info

    def options(self,namespaces):
        info = self.parser.options(namespaces)
        return info

    def getSSHConf(self, name):
        temp = self.parser.get("sshs", name);
        temp = temp.split(',')

        auth = temp[0].strip();
        info = {
            'authMode': auth,
            'name': temp[1].strip(),
            'port': temp[3].strip()
        }
        if auth == 'rsaauth':
            info['authKeyFile'] = temp[2].strip();
            info['passwd'] = ''
        else:
            info['passwd'] =  temp[2].strip()
            info['authKeyFile'] =  ''

        return info

    def getNodeInfo(self,nodename):
        res = {
            'name',''
            'host',''
            'sshname',''
        }
        return res


class SnowballConfig(AbstractConfig):
    def getClusters(self):
        info = self.options('cluster')
        return info

    def getClusterReplicas(self):
        clusters = self.items('cluster')
        itemArr = []
        for temp in clusters:
            name, infostr = temp
            shareds = infostr.split(';')
            for share in shareds:
                relicas = share.strip().split(',')
                for relica in relicas:
                    relica = relica.strip()
                    itemArr.append(relica)

        return itemArr

    def getNodeInfo(self, nodename):

        if self.has_option('nodes', nodename) == False:
            return False

        rawinfo = self.get("nodes", nodename)
        data = rawinfo.split(',')
        # print(data.has_key(4))

        host = data[0].strip()
        sshname = data[1].strip()
        # print("sshname",sshname)

        if self.has_option(nodename,'tcp_port'):
            tcp_port = self.get(nodename,'tcp_port')
        elif self.has_option('snowballConf','tcp_port'):
            tcp_port = self.get('snowballConf', 'tcp_port')
        else:
            tcp_port = '9000'

        if self.has_option(nodename,'http_port'):
            http_port = self.get(nodename,'http_port')
        elif self.has_option('snowballConf','http_port'):
            http_port = self.get('snowballConf', 'http_port')
        else:
            http_port = '8123'

        if self.has_option(nodename,'interserver_http_port'):
            interserver_http_port = self.get(nodename,'interserver_http_port')
        elif self.has_option('snowballConf','interserver_http_port'):
            interserver_http_port = self.get('snowballConf', 'interserver_http_port')
        else:
            interserver_http_port = '9009'

        info={
            'name': nodename,
            'host': host,
            'sshname':sshname,
            'tcp_port':tcp_port,
            'http_port':http_port,
            'interserver_http_port':interserver_http_port,
        }
        return info

    def getSnowballBaseConf(self):
        f = open(selfPath+'/config/snowball.config.xml.tpl', 'r')
        xmlstr = f.read()

        snowballconf = xmltodict.parse(xmlstr)
        # 全局覆盖
        tempConfs = self.items('snowballConf')
        # print(tempConfs)
        for newconfitem in tempConfs:
            name, value = newconfitem;
            # print(name +':'+ value)
            snowballconf['yandex'][name] = value

        # snowballconf = self.bindCluster(snowballconf)
        snowballconf['yandex']['remote_servers'] = ''
        return  snowballconf

    def getSnowballNodeConf(self, nodename):
        snowballbaseConf = self.getSnowballBaseConf()
        if self.has_section(nodename) == True:
            tempConfs = self.items(nodename)
            # print(tempConfs)
            for newconfitem in tempConfs:
                name, value = newconfitem;
                # print(name +':'+ value)
                snowballbaseConf['yandex'][name] = value

        return  snowballbaseConf

    pass

class ZookeeperConf(AbstractConfig):
    # def getNodes(self):
    #     rawinfo = self.items('nodes')
    #     # nodes = rawinfo.split(',')
    #     # for k,v in enumerate(nodes):
    #     #     nodes[k] = v.strip()
    #
    #     return rawinfo

    def getNodeInfo(self, nodename):

        if self.has_option('nodes', nodename) == False:
            return False

        rawinfo = self.get("nodes", nodename)
        data = rawinfo.split(',')
        # print(data.has_key(4))

        servid = data[0].strip()
        host = data[1].strip()
        clientPort = data[2].strip()
        port2 = data[3].strip()
        port3 = data[4].strip()
        sshname = data[5].strip()
        # print("sshname",sshname)
        info={
            'name': nodename,
            'servid': servid,
            'host': host,
            'clientPort': clientPort,
            'leaderPort': port2,
            'listenPort': port3,
            'sshname':sshname,
        }
        return info

    def getNodeZookeeperConf(self, nodename):
        temps = self.items('zookeeper')
        nodeInfo = self.getNodeInfo(nodename)
        confs = {}
        for temp in temps:
            k,v = temp
            # print (k, v)
            confs[k] = v

        confs['clientPort'] = nodeInfo['clientPort']
        return confs
        # print(confs)

    pass


snowballConf = SnowballConfig(selfPath+'/config/conf.ini')
zookeeperConf = ZookeeperConf(selfPath+'/config/conf.zookeeper.install.ini')

class ClusterConfig(AbstractConfig):
    def getClusetName(self):
        name = ''
        if self.has_option('cluster','name'):
            name = self.get('cluster','name')
        return name;
        # return self.get()
    def getClusterNodes(self):
        rawinfo = self.get('cluster','nodes')
        nodes = rawinfo.split(',')
        for k,v in enumerate(nodes):
            nodes[k] = v.strip()

        return nodes
    def getDefaultDatabase(self):
        res = self.get('cluster', 'default_database')
        database = res.split(',')
        for k,v in enumerate(database):
            # print(k,v)
            database[k] = v.strip()
        # if len(database) =
        return database

    def getClusterConfig(self):

        clustername = self.getClusetName()
        nodes = self.getClusterNodes()
        # print(nodes)
        databases = self.getDefaultDatabase()
        if(len(databases) > 2):
            raise Exception('Cluster Nodes Error !')

        tempconfs = []
        for i,nodename in enumerate(nodes) :
            tempconf = {}
            tempconf['internal_replication'] = 'true'

            node = snowballConf.getNodeInfo(nodename)

            if(type(node) == bool):
                raise Exception('Cluster Node :' + nodename + ' is not exist !')

            if len(databases) == 1:
                replica = {
                    'host': node['host'],
                    'port': node['tcp_port'],
                    'default_database': databases[0]
                }
            elif len(databases) == 2:
                if (i < len(nodes) - 1):
                    backupnodename = nodes[i+1]
                else:
                    backupnodename = nodes[0]

                backupnoden = snowballConf.getNodeInfo(backupnodename)
                replica = [
                    {
                        'host': node['host'],
                        'port': node['tcp_port'],
                        'default_database': databases[0]
                    },
                    {
                        'host': backupnoden['host'],
                        'port': backupnoden['tcp_port'],
                        'default_database': databases[1]
                    }
                ]
            tempconf['replica'] = replica
            tempconfs.append(tempconf)
        return clustername, tempconfs
    pass


clusterConfig = ClusterConfig(selfPath+'/config/conf.cluster.create.ini')
