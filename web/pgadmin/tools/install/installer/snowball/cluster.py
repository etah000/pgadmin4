# coding: utf-8


import sys, os
from pgadmin.tools.install.config import snowballConf as baseconf
from pgadmin.tools.install.config import clusterConfig as clusterconf
from pgadmin.tools.install.installer.snowball.helper import helper

clusternodes = clusterconf.getClusterNodes()
clustername = clusterconf.getClusetName()
defauleDatabases = clusterconf.getDefaultDatabase()
serverodes = baseconf.options('nodes')

class Cluster():
    def create(self):
        self.createNewCluster()
        pass
    def createNewCluster(self):
        # print(clusternodes)
        print('\r\nStep-1: Check node ssh connection .......')
        self.__checkNodesSystemInfo()

        print('\r\nStep-2: Prepare for node ....')
        self.__prepareForNodes()

        print('\r\nStep-3: Restart Server....')
        self.__restartServer()

        print('\r\nStep-4: Check Cluster Status....')
        self.__checkClusterStatus()

        pass

    def __checkNodesSystemInfo(self):
        global clusternodes

        try:
            allNodeSupporedToInstall = True
            unSupportNode = ''
            sys.stdout.write('待安装的节点:')
            print(clusternodes)

            diff = list(set(clusternodes).difference(set(serverodes)))
            if (len(diff) > 0):
                print('以下节点不存在')
                print(diff)
                raise Exception('集群配置中有不符合的界定')

            if(len(clusternodes) < 3):
                print('集群数量不符合要求')
                raise Exception('集群数量不符合要求')

            if (len(defauleDatabases) >2):
                print('副本数量不符合要求')
                raise Exception('副本数量不符合要求')

            tempSuccessNode = []

            for i, nodename in enumerate(clusternodes):
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

                res = helper.clusterIsExist(nodename, clustername);

                if  res == False:
                    print('~ClusterIsExist: \033[1;32m No \033[0m')
                    tempSuccessNode.append(nodename)
                else:
                    print('~ClusterIsExist: \033[1;31mYes\033[0m')
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
        for nodename in clusternodes:

            print('-2.1 Prepare default database : ' + nodename)
            self.__prepareDefaultDatabase(nodename)

            print('-2.2 Prepare Config.xml file : ' + nodename)
            self.__prepareConfigXml(nodename)

    def __prepareDefaultDatabase(self,nodename):
        for dbname in defauleDatabases:
            helper.createDatabaseBase(nodename,dbname)

        pass
    def __prepareConfigXml(self,nodename):
        helper.createNewClusterXml(nodename)
        pass

    def __restartServer(self):
        for nodename in clusternodes:
            helper.restartSnowballServ(nodename)
            # helper.verifySnowballStatus(nodename)

    def __checkClusterStatus(self):
        for nodename in clusternodes:
            res = helper.clusterIsExist(nodename, clustername)
            if res == False:
                print('~Cluster Created: \033[1;31mFailure\033[0m')
                self.rollback()
                break
            else:
                print('~Cluster Created: \033[1;32mSuccess\033[0m')


    def __rollback(self):
        print('Cluster Created RollBack:')
        for nodename in clusternodes:
            res = helper.deleteSnowballCluster(nodename, clustername)
            res = helper.restartSnowballServ(nodename, clustername)
            print(res)


cluster = Cluster()
