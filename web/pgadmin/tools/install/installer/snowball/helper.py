# coding: utf-8

import xmltodict,json
from pgadmin.tools.install.installer.snowball.node import Node
from pgadmin.tools.install.installer.snowball.executor import Cent7Executor

from pgadmin.tools.install.config import clusterConfig , snowballConf

class Helper():

    nodes = {}
    executors = {}
    checkedList = {}

    def getNode(self, nodename):
        #if self.nodes.has_key(nodename) != True:
        if nodename not in self.nodes:
            self.nodes[nodename] = Node(nodename)
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
                    self.executors[nodename] = Cent7Executor()
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


    def prepareDependency(self,nodename,spath,remoteSoftdir):
        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)
        return executor.prepareDependency(node,spath,remoteSoftdir)

    def prepareFirewalldRule(self, nodename):
        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)
        return executor.prepareFirewalldRule(node)

    def prepareDataDisk(self,nodename):
        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)
        return executor.prepareDataDisk(node)

    def copyInstallFile(self,nodename,spath):

        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)
        return executor.copyInstallFile(node,spath)

    def installSnowballServ(self, nodename):

        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)

        return executor.installSnowballServ(node)

    def startSnowballServ(self, nodename):

        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)

        return executor.startSnowballServ(node)

    def restartSnowballServ(self, nodename):

        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)

        return executor.restartSnowballServ(node)

    def verifySnowballStatus(self, nodename):

        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)

        return executor.verifySnowballStatus(node)

    def replaceLicence(self, nodename, filename):

        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)

        return executor.replaceLicence(node, filename)


    def clusterIsExist(self,nodename, clustername):
        node = self.getNode(nodename)
        return  node.clusterIsExist(clustername)

    def createDatabaseBase(self,nodename,databasename):
        node = self.getNode(nodename)
        return  node.createDatabase(databasename)

    def createNewClusterXml(self, nodename):
        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)

        conf = executor.getRemoteConfigXml(node)
        snowballconf = xmltodict.parse(conf)

        cluster = snowballconf['yandex']['remote_servers'];
        newclustername, newShards = clusterConfig.getClusterConfig()

        if cluster == None:
            cluster = {}

        cluster[newclustername] = {'shard':newShards}

        snowballconf['yandex']['remote_servers'] = cluster

        return executor.updateRomoteConfigXml(node,snowballconf)

    def deleteSnowballCluster(self, nodename, clustername):
        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)

        conf = executor.getRemoteConfigXml(node)
        snowballconf = xmltodict.parse(conf)

        clusters = snowballconf['yandex']['remote_servers'];
        for k in clusters.keys():
            print(k)
            if k == clustername :
                del clusters[k]
                break
        snowballconf['yandex']['remote_servers'] = clusters

        res = executor.updateRomoteConfigXml(node, snowballconf)
        # xmlfile = xmltodict.unparse(snowballconf, pretty=True);
        # print(xmlfile)
        return  res;
    def getIP(self,name,hosts):
        for host in hosts:
            if host['name'] == name :
                return host['ip']
        return '0.0.0.0'


helper = Helper()
