# coding: utf-8

import xmltodict
from .abstract import AbstractHelp

from serv.node.snowball import SnowballNode
from serv.conf import clusterConfig, snowballConf


class SnowballBackupHelper(AbstractHelp):

    def getNode(self, nodename):
        if self.nodes.has_key(nodename) != True:
            self.nodes[nodename] = SnowballNode(nodename)
        return self.nodes[nodename]

    def prepareDependency(self, nodename):
        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)
        return executor.prepareSnowballDependency(node)

    def prepareFirewalldRule(self, nodename):
        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)
        return executor.prepareSnowballFirewalldRule(node)

    def copyInstallFile(self, nodename):
        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)
        return executor.copySnowballInstallFile(node)

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

    def stopSnowballServ(self, nodename):
        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)
        return executor.stopSnowballServ(node)

    def getSnowballServStatus(self, nodename):
        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)
        return executor.getSnowballServStatus(node)

    def replaceLicence(self, nodename, filename):
        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)
        return executor.replaceSnowballLicence(node, filename)

    def clusterIsExist(self, nodename, clustername):
        node = self.getNode(nodename)
        return node.clusterIsExist(clustername)

    def createDatabaseBase(self, nodename, databasename):
        node = self.getNode(nodename)
        return node.createDatabase(databasename)

    def updateSnowballConfigXml(self, nodename, key, value):
        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)

        conf = executor.getRemoteSnowballConfigXml(node)
        snowballServConf = xmltodict.parse(conf)

        tempConf = snowballServConf['yandex'][key]
        if tempConf == None:
            tempConf = {}
        tempConf = value
        snowballServConf['yandex'][key] = tempConf
        return executor.updateRomoteSnowballConfigXml(node, snowballServConf)

    def createNewClusterXml(self, nodename):
        conf = {}
        newclustername, newShards = clusterConfig.getClusterConfig()
        conf[newclustername] = {'shard': newShards}
        return self.updateSnowballConfigXml(nodename, 'remote_servers', conf)

    def deleteSnowballCluster(self, nodename, clustername):
        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)

        conf = executor.getRemoteSnowballConfigXml(node)
        snowballconf = xmltodict.parse(conf)

        clusters = snowballconf['yandex']['remote_servers']
        for k in clusters.keys():
            if k == clustername:
                del clusters[k]
                break
        snowballconf['yandex']['remote_servers'] = clusters

        res = executor.updateRomoteSnowballConfigXml(node, snowballconf)
        return res

    def uploadMonitorClientFile(self, nodename):
        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)
        return executor.uploadMonitorClientFile(node)

    def installMonitorClient(self, nodename):
        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)
        return executor.installMonitorClient(node)

    def uploadNtpdClientFile(self, nodename):
        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)
        return executor.uploadNtpdClientFile(node)

    def installNtpdClient(self, nodename):
        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)
        return executor.installNtpdClient(node)

    def changeSnowballZookeeper(self, nodename):
        node = self.getNode(nodename)
        executor = self.getExecuter(nodename)
        conf = executor.getRemoteSnowballConfigXml(node)
        # print(conf)
        xmlconf = xmltodict.parse(conf)
        zookeeper = {
            '@incl': 'zookeeper-servers',
            '@optional': 'true'
        }
        zookeepernode = snowballConf.getZookeeperNode()
        zookeeper['node'] = zookeepernode
        print(zookeeper)
        xmlconf['yandex']['zookeeper'] = zookeeper
        # xmlfile = xmltodict.unparse(xmlconf, pretty=True);
        # print(xmlfile)
        return executor.updateRomoteSnowballConfigXml(node, xmlconf)


snowballHelper = SnowballHelper()
