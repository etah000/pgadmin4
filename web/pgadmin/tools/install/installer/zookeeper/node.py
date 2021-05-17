# coding: utf-8
from pgadmin.tools.install.installer.node import AbstractNode

class Node(AbstractNode):
    # zookeeperconf = {}
    conf = {}
    info = {}
    jsonCfg = {}
    servers = []
    dbStatus = False

    def __init__(self, name,jsonCfg):
        self.name = name;
        self.jsonCfg = jsonCfg;
        infoT = self.getNodeInfo(name,jsonCfg['zookeeper']['nodes'])
        info = {'name': infoT['name'], 'servid': infoT['order'], 'host': self.getIP(infoT['ssh'],jsonCfg['hosts']), 'clientPort': infoT['port1'], 'leaderPort': infoT['port2'], 'listenPort': infoT['port3'], 'sshname': infoT['ssh']}

        #{'name': 'zk001', 'servid': '1', 'host': '192.168.52.128', 'clientPort': '2181', 'leaderPort': '2888', 'listenPort': '3888', 'sshname': 'node1'}
        self.host = info['host']
        sshT = self.getSSHConf(info['sshname'],jsonCfg['hosts'])
        self.ssh = {'authMode': '1', 'name': sshT['user'], 'port': sshT['port'], 'passwd': sshT['password'], 'authKeyFile': ''}
        self.info = info;
        self.conf = {'tickTime': jsonCfg['zookeeper']['tickTime'], 'initLimit': jsonCfg['zookeeper']['initLimit'], 'syncLimit': jsonCfg['zookeeper']['syncLimit'], 'dataDir': jsonCfg['zookeeper']['dataDir'], 'clientPort': jsonCfg['zookeeper']['clientPort']}
        self.servers = self.getServers(jsonCfg['zookeeper']['nodes'])
    def getInfo(self):
        return self.info
    def getConf(self):
        return self.conf
    #根据名称 找ip
    def getIP(self,name,hosts):
        for host in hosts:
            if host['name'] == name :
                return host['ip']
        return '0.0.0.0'
    #根据名称 节点信息
    def getNodeInfo(self,name,zknodes):
        for zknode in zknodes:
            if zknode['name'] == name :
                return zknode
        return {}
    #根据sshname找条目
    def getSSHConf(self,sshname,hosts):
        for host in hosts:
            if host['name'] == sshname :
                return host
        return {}
    def getServers(self,zknodes):
        servers = []
        for zknode in zknodes:
            servers.append({'name': zknode['name'], 'servid': zknode['order'], 'host': self.getIP(zknode['ssh'],self.jsonCfg['hosts']), 'clientPort': zknode['port1'], 'leaderPort': zknode['port2'], 'listenPort': zknode['port3'], 'sshname': zknode['ssh']})
        return servers
