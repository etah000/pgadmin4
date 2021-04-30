# coding: utf-8

import sys, os
from pgadmin.tools.install.config import zookeeperConf as conf
from pgadmin.tools.install.installer.zookeeper.helper import helper

nodes = conf.options('nodes')

class Processer():

    def install(self,spath,remoteSoftdir):
        try:
            self.installZookeeper(spath,remoteSoftdir)
        except Exception as e:
            print(e)

    def installZookeeper(self,spath,remoteSoftdir):
        print('Start Install Zookeeper ....... ')

        print('\r\nStep-1: Check node ssh connection .......')
        self.__checkNodesSystemInfo()

        print('\r\nStep-2: Prepare for node ....')
        self.__prepareForNodes(spath,remoteSoftdir)
        # #
        # print('\r\nStep-3: Install zookeeper on Node ....')
        # self.__installZookeeperOnNodes()
        # #
        print("\r\nStep-4: Start zookeeper server ....")
        self.__startZookeeperServ()

        print("\r\nStep-5: Verify zookeeper server status")
        self.__verifyZookeeperServStatus()

    def __checkNodesSystemInfo(self):
        global nodes
        allNodeSupporedToInstall = True
        unSupportNode = ''
        sys.stdout.write('待安装的节点:')
        print(nodes)
        tempSuccessNode = []
        # if 1==1:
        try:
            for i, nodename in enumerate(nodes):
                # SSH 连通性检查
                # msg = 'Connect to %s: %s ' % (nodename, self.host);
                msg = 'Connect to %s: ' % (nodename);
                sys.stdout.write(msg)
                res = helper.checkNodeSSHConnection(nodename)

                if res == False:
                    print('\r\n~\033[1;31mConnect Failure:\033[0m ' + nodename)
                else:
                    print('\r\n~\033[1;32mConnect Success:\033[0m ' + nodename + ':' + res)

                # 操作系统是否支持检查
                res = helper.isSportedToInstall(nodename)
                if res != False:
                    print('~IsSported: \033[1;32mSuccess\033[0m')
                    tempSuccessNode.append(nodename)
                else:
                    print('~IsSported: \033[1;31mFailure\033[0m')
                    allNodeSupporedToInstall = False
                    unSupportNode = unSupportNode + '  #' + nodename

            sys.stdout.write('\r\n符合安装条件节点:')
            print(tempSuccessNode)

            nodes = tempSuccessNode
            if allNodeSupporedToInstall == False:
                nodes = []
                print('以下节点链接异常:\033[1;31m' + unSupportNode + '\033[0m')
                raise Exception('服务器链接异常, 请检查服务配置')
        except Exception as e:
            print('Exception:' +e)
            raise e
        pass

    def __prepareForNodes(self,spath,remoteSoftdir):

        for nodename in nodes:

            print('-2.1 Prepare firewalld rules node : ' + nodename)
            self.__prepareFirewalldRules(nodename)
            #
            print('-2.2 Prepare install file ....')
            self.__copyInstallFileToNodes(nodename,spath,remoteSoftdir)

    def __startZookeeperServ(self):
        for nodename in nodes:
            helper.startZookeeperServ(nodename)
            # helper.verifyZookeeperStatus(nodename)
        pass

    def __verifyZookeeperServStatus(self):
        for nodename in nodes:
            helper.verifyZookeeperStatus(nodename)

    def __prepareFirewalldRules(self,nodename):

        helper.prepareFirewalldRule(nodename)

    def __copyInstallFileToNodes(self,nodename,spath,remoteSoftdir):

        helper.copyInstallFile(nodename,spath,remoteSoftdir)


zookeeperProcesser = Processer()
