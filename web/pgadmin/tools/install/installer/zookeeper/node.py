# coding: utf-8

from pgadmin.tools.install.config import zookeeperConf as conf
from pgadmin.tools.install.installer.node import AbstractNode

class Node(AbstractNode):
    # zookeeperconf = {}
    conf = {}
    info = {}
    dbStatus = False

    def __init__(self, name):
        self.name = name;
        info = conf.getNodeInfo(name)
        ssh = conf.getSSHConf(info['sshname'])
        self.host = info['host']
        self.ssh = ssh
        self.info = info;
        self.conf = conf.getNodeZookeeperConf(name)
    def getInfo(self):
        return self.info
    def getConf(self):
        return self.conf

