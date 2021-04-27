# coding: utf-8

import sys

# from serv import snowballConf as conf
from serv.conf import snowballConf as conf
from serv.helper import snowballBackupHelper as helper

nodes = conf.getNodeNameList()


class SnowballBackupFade():

    def install(self):
        try:
            self.installSnowball()
        except Exception as e:
            print(e)

    def changeZookeeper(self):
        global nodes
        print('\r\nStart replace Snowball zookeeper....... ')
        # sys.stdout.write('待安装的节点:')
        try:

            print('\r\nStep-1: Check node ssh connection .......')
            self.checkNodesSystemInfo(nodes)

            print('\r\nStep-2: Check node ssh connection .......')
            self.changeSnowballZookeeper(nodes)

            print("\r\nStep-3: reStart snowball server ....")
            self.restartSnowballServ(nodes)

        except Exception as e:
            print('ERROR:', e)
            raise e

    def installSnowballBackup(self):
        global nodes
        print('\r\nStart Install Snowball Backup ....... ')
        sys.stdout.write('待安装的节点:')
        print(nodes)
        try:

            print('\r\nStep-1: Check node ssh connection .......')
            self.checkNodesSystemInfo(nodes)

            print('\r\nStep-2: Prepare for node ....')
            self.__prepareForNodes(nodes)

            print('\r\nStep-3: Install snowball on Node ....')
            self.__installSnowballOnNodes(nodes)
            #
            # print("\r\nStep-4: Start snowball server ....")
            # self.startSnowballServ(nodes)
            #
            # print("\r\nStep-5: Verify snowball server status ....")
            # self.checkSnowballServStatus(nodes)

        except Exception as e:
            print('ERROR:', e)
            raise e

    def checkNodesSystemInfo(self, nodeNameArr):
        for nodename in nodeNameArr:
            res = helper.checkNodeSSHConnection(nodename)
            if res == False:
                print('\r\n~\033[1;31m~Connect Failure:\033[0m ' + nodename)
                raise Exception('Connect Failure:'+nodename)
            else:
                print('\r\n~\033[1;32m~Connect Success:\033[0m ' + nodename + ':' + res)

            res = helper.isSportedToInstall(nodename)
            # print(res)
            if res != False:
                print('\r\n~\033[1;32m~Os Support Success:\033[0m ' + nodename)
            else:
                print('\r\n~\033[1;31m~Os Support Failure:\033[0m ' + nodename + ':' + res)
                raise Exception('Os Support Failure:' + nodename)

    def __prepareForNodes(self, nodeNameArr):
        for nodename in nodeNameArr:
            print('-2.1 Prepare soft dependency for node : ' + nodename)
            helper.prepareDependency(nodename)

            print('-2.2 Prepare firewalld rules node : ' + nodename)
            helper.prepareFirewalldRule(nodename)
            #
            print('-2.3 Prepare install file ....')
            helper.copyInstallFile(nodename)

    def __installSnowballOnNodes(self, nodeNameArr):
        for nodename in nodeNameArr:
            helper.installSnowballServ(nodename)

    def startSnowballServ(self, nodeNameArr):
        for nodename in nodeNameArr:
            helper.startSnowballServ(nodename)

    def checkSnowballServStatus(self, nodeNameArr):
        for nodename in nodeNameArr:
            helper.getSnowballServStatus(nodename)

    def restartSnowballServ(self, nodeNameArr):
        for nodename in nodeNameArr:
            helper.restartSnowballServ(nodename)

    def stopSnowballServ(self, nodeNameArr):
        for nodename in nodeNameArr:
            helper.stopSnowballServ(nodename)

    def changeSnowballZookeeper(self, nodeNameArr):
        for nodename in nodeNameArr:
            helper.changeSnowballZookeeper(nodename)


snowballBackupFade = SnowballBackupFade()
