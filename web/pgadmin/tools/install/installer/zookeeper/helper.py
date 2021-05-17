# coding: utf-8

import xmltodict,json
from pgadmin.tools.install.installer.zookeeper.node import Node
from  pgadmin.tools.install.installer.zookeeper.executor.abstract import AbstractExecutor

# from config import clusterConfig , snowballConf

class Helper():

    nodes = {}
    jsonCfg = {}
    executors = {}
    checkedList = {}
    def __init__(self, jsonCfg):
        self.jsonCfg = jsonCfg

    def getNode(self, nodename):
        #if self.nodes.has_key(nodename) != True:
        if nodename not in self.nodes:
            self.nodes[nodename] = Node(nodename,self.jsonCfg)#new node
        return self.nodes[nodename]

    def getExecuter(self,nodename):
        node = self.getNode(nodename)
        #if self.checkedList.has_key(nodename) != True:
        if nodename not in self.checkedList:
            self.checkNodeSSHConnection(nodename)

        #if self.executors.has_key(nodename) != True:
        if nodename not in self.executors:
            if(node.os['name'] == 'centos'):
                osversion = float(node.os['version'][0:3])
                if(osversion >= 7):
                    self.executors[nodename] = AbstractExecutor()
                else:
                    # self.executors[nodename] = Cent6Executor()
                    raise Exception('Centos6 can not Support')
                    return False
            elif(node.os == 'ubuntu'):
                # self.executors[nodename] = UbuntuExecutor()
                raise Exception('Ubuntu can not Support')
                return False
            else:
                raise Exception('Unknow OS can not Support')
                return False

        return self.executors[nodename];


    def checkNodeSSHConnection(self, nodename):
        node = self.getNode(nodename)

        res =  node.CheckSSHConnectAndGetOsInfo()
        self.checkedList[nodename] = True

        if res == True:
            return node.os['name']+':'+node.os['version']
        else:
            return False

    def isSportedToInstall(self, nodename):
        node = self.getNode(nodename)
        # 连通性检查
        if node.status != True:
            return False
        # 支持的操作系统检查
        osname = node.os['name']
        version = node.os['version']
        if (osname == 'centos'):
            if float(version) > 6.4:
                return True
            else:
                return False
        else:
            return False


    def prepareDependency(self,nodename):
        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)
        return executor.prepareDependency(node)

    def prepareFirewalldRule(self, nodename):
        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)
        return executor.prepareFirewalldRule(node)

    def copyInstallFile(self,nodename,spath,remoteSoftdir,remoteAppdir,softlist):

        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)
        return executor.copyInstallFile(node,spath,remoteSoftdir,remoteAppdir,softlist)

    def installZookeeperServ(self, nodename,remoteConfDir):

        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)

        return executor.installSnowballServ(node,remoteConfDir)

    def startZookeeperServ(self, nodename):

        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)

        return executor.startZookeeperServ(node)

    def restartZookeeperServ(self, nodename):

        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)

        return executor.restartSnowballServ(node)

    def verifyZookeeperStatus(self, nodename):

        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)

        return executor.verifyZookeeperStatus(node)

