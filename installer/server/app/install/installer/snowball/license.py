# coding: utf-8


import sys, os

from pgadmin.tools.install.config import snowballConf as baseconf
from pgadmin.tools.install.installer.snowball.helper import helper
from pgadmin.tools.install.installer.common import GetSelfPath

appDir = GetSelfPath();

serverodes = baseconf.options('nodes')

class License():

    def deploy(self):
        print('\r\nStep-1: Check node ssh connection .......')
        self.__checkNodesSystemInfo()

        print('\r\nStep-2: Prepare for node ....')
        self.__prepareForNodes()

        print('\r\nStep-3: Restart Server....')
        self.__restartServer()

        pass

    def __checkNodesSystemInfo(self):
        global serverodes

        try:
            allNodeSupporedToInstall = True
            unSupportNode = ''
            sys.stdout.write('待安装的节点:')
            print(serverodes)
            tempSuccessNode = []

            for i, nodename in enumerate(serverodes):
                # SSH 连通性检查
                msg = 'Connect to %s: ' % (nodename);
                sys.stdout.write(msg)
                res = helper.checkNodeSSHConnection(nodename)

                if res == False:
                    print('\r\n~\033[1;31mSSHConnect Failure:\033[0m ' + nodename)
                else:
                    print('\r\n~\033[1;32mSSHConnect Success:\033[0m ' + nodename +':'+ res)

                # 操作系统是否支持检查
                res = helper.isSportedToInstall(nodename)
                if  res != False:
                    print('~OsIsSported: \033[1;32mSuccess\033[0m')
                    tempSuccessNode.append(nodename)
                else:
                    print('~OsIsSported: \033[1;31mFailure\033[0m')
                    allNodeSupporedToInstall = False
                    unSupportNode = unSupportNode + '  #' + nodename


            sys.stdout.write('\r\n符合安装条件节点:')
            print(tempSuccessNode)

            nodes = tempSuccessNode
            if allNodeSupporedToInstall == False:
                nodes = []
                print('以下节点链接异常:\033[1;31m' + unSupportNode + '\033[0m')
                raise Exception('服务器链接异常, 请检查服务配置')
            # sys.stdout.write('\r\n集群信息检查:')
        except Exception as e:
            print('Exception:' +e)
            # raise e

    def __prepareForNodes(self):
        for nodename in serverodes:
            print('-2.1 Prepare License.xml file : ' + nodename)
            self.__prepareLicenseXml(nodename)

    def __prepareLicenseXml(self, nodename):
        licensefile = appDir+'/config/snowball.license.xml.tpl'
        helper.replaceLicence(nodename, licensefile)
        pass

    def __restartServer(self):
        for nodename in serverodes:
            helper.restartSnowballServ(nodename)
            helper.verifySnowballStatus(nodename)

license = License()
