# coding: utf-8
from pgadmin.tools.install.installer.snowball.helper import Helper
import sys, os

class Processer():

    def install(self,spath,remoteSoftdir,remoteConfDir,softlist,nodes,jsonCfg):
        try:
            self.installSnowball(spath,remoteSoftdir,remoteConfDir,softlist,nodes,jsonCfg)
        except Exception as e:
            print(e)

    def installSnowball(self,spath,remoteSoftdir,remoteConfDir,softlist,nodes,jsonCfg):

        print('\r\nStart Install Snowball ....... ')

        print('\r\nStep-1: Check node ssh connection .......')
        self.__checkNodesSystemInfo(nodes,jsonCfg)

        print('\r\nStep-2: Prepare for node ....')
        self.__prepareForNodes(spath,remoteSoftdir,nodes,softlist,jsonCfg)

        print('\r\nStep-3: Install snowball on Node ....')
        self.__installSnowballOnNodes(remoteConfDir,nodes,jsonCfg)
        #
        print("\r\nStep-4: Start snowball server ....")
        self.__startSnowballServ(nodes,jsonCfg)
        #
        print("\r\nStep-5: Verify snowball server status ....")
        self.__verifySnowballServStatus(nodes,jsonCfg)

    def __checkNodesSystemInfo(self,nodes,jsonCfg):
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
                res = Helper(jsonCfg).checkNodeSSHConnection(nodename)

                if res == False:
                    print('\r\n~\033[1;31mConnect Failure:\033[0m ' + nodename)
                else:
                    print('\r\n~\033[1;32mConnect Success:\033[0m ' + nodename +':'+ res)

                # 操作系统是否支持检查
                res = Helper(jsonCfg).isSportedToInstall(nodename)
                if  res != False:
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

            # sys.stdout.write('\r\n集群信息检查:')
            # replicas = conf.getClusterReplicas()
            # print(replicas)
            #
            # diff = list(set(replicas).difference(set(tempSuccessNode)))
            # if len(diff) == 0 :
            #     print('集群配置节点符合要求')
            # else :
            #     sys.stdout.write('有'+ str(len(diff)) +' 节点不符合要求:')
            #     print(diff)
            #     raise Exception('集群节点异常, 请检查集群配置')

        except Exception as e:
            print('Exception:' +e)
            raise e

    def __prepareForNodes(self,spath,remoteSoftdir,nodes,softlist,jsonCfg):

        for nodename in nodes:
            # print('-- Prepare data disk ....')
            # self.__prepareDataDisk(nodename)

            #print('-2.1 Prepare soft dependency for node : ' + nodename)
            #self.__prepareDependencyForNode(nodename,spath,remoteSoftdir)

            print('-2.2 Prepare firewalld rules node : ' + nodename)
            self.__prepareFirewalldRules(nodename,jsonCfg)
            #
            print('-2.3 Prepare install file ....')
            self.__copyInstallFileToNodes(nodename,spath,remoteSoftdir,softlist,jsonCfg)



    def __prepareDataDisk(self,nodename,jsonCfg):

        Helper(jsonCfg).prepareDataDisk(nodename)

    def __prepareDependencyForNode(self,nodename,spath,remoteSoftdir,jsonCfg):

        Helper(jsonCfg).prepareDependency(nodename,spath,remoteSoftdir)

    def __prepareFirewalldRules(self,nodename,jsonCfg):

        Helper(jsonCfg).prepareFirewalldRule(nodename)

    def __copyInstallFileToNodes(self,nodename,spath,remoteSoftdir,softlist,jsonCfg):

        Helper(jsonCfg).copyInstallFile(nodename,spath,remoteSoftdir,softlist)

    def __installSnowballOnNodes(self,remoteConfDir,nodes,jsonCfg):
        for nodename in nodes:
            Helper(jsonCfg).installSnowballServ(nodename,remoteConfDir)

    def __startSnowballServ(self,nodes,jsonCfg):
        for nodename in nodes:
            Helper(jsonCfg).startSnowballServ(nodename)

    def __verifySnowballServStatus(self,nodes,jsonCfg):
        for nodename in nodes:
            Helper(jsonCfg).verifySnowballStatus(nodename)




