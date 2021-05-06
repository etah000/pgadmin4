# coding: utf-8

import xmltodict
from pgadmin.tools.install.installer.common import GetSelfPath
from pgadmin.tools.install.config import zookeeperConf
from pgadmin.utils import get_storage_directory

#selfPath = GetSelfPath()
#softPath = selfPath + '/soft/'
#confPath = selfPath + '/config/'
#remoteSoftdir = '/app/soft/'
#remoteAppdir = '/app/zookeeper/'
#remoteJdkdir = '/app/jdk/'

class AbstractExecutor():
    def getZookeeperFile(self):
        return {
            'zookeeper':'',
            'jdk':''
        }
    pass

    def prepareFirewalldRule(self, node):
        conf = node.getInfo()
        clientPort = conf['clientPort']
        leaderPort = conf['leaderPort']
        listenPort = conf['listenPort']

        cmd = 'firewall-cmd --add-port=%s/tcp --permanent &&'%(clientPort)
        cmd = cmd + 'firewall-cmd --add-port=%s/tcp --permanent &&'%(leaderPort)
        cmd = cmd + 'firewall-cmd --add-port=%s/tcp --permanent &&'%(listenPort)
        cmd = cmd + 'firewall-cmd --reload'
        res = node.call(cmd)
        print(res)
        # print('check checkFirewalld ...', node)
        return True

    def copyInstallFile(self, node,spath,remoteSoftdir,remoteAppdir):
        cmd = ''
        cmd = cmd + 'mkdir -p /app && mkdir -p ' + remoteSoftdir + '&& '
        cmd = cmd + 'rm -rf /app/jdk && rm -rf /app/jdk1.8.0_201 && rm -rf /app/apache-zookeeper-3.5.7-bin && rm -rf /app/zookeeper'
        node.call(cmd)

        softlist = self.getZookeeperFile();
        for soft, filename in softlist.items():
            fullFilename = get_storage_directory()+ spath + filename
            res = node.put(fullFilename, remoteSoftdir)
            print(res)
        self.unzipInstallFile(node,remoteSoftdir)
        self.cpZookerCfgFile(node,remoteAppdir)
        self.makeIdfile(node)
        return True

    def cpZookerCfgFile(self, node,remoteAppdir):
        confs = node.getConf()
        content = '#zookeeper cfg file'+ '\n'
        for k in confs:
            content = content + k + '=' + confs[k] + '\n'
        content = content + '\n'

        nodes = zookeeperConf.options('nodes')
        for nodename in nodes:
            temp = zookeeperConf.getNodeInfo(nodename)
            str = "server.%s=%s:%s:%s" % (temp['servid'], temp['host'], temp['leaderPort'], temp['listenPort'])
            content = content + str + '\n'
        print(content);
        filename = remoteAppdir + 'conf/zoo.cfg'
        print(filename)
        res = node.write(content, filename)
        return res

    def makeIdfile(self,node):
        confs = node.getConf()
        info = node.getInfo()
        servid = info['servid']
        datadir = confs['dataDir']
        cmd = 'mkdir -p ' + datadir + '; '

        cmd = cmd + 'echo "%s" > %s/%s'%(servid,datadir,'myid')
        res = node.call(cmd)
        print(res)

    def unzipInstallFile(self,node,remoteSoftdir):

        softlist = self.getZookeeperFile();

        javafile = softlist['jdk']
        zkfile = softlist['zookeeper']

        remoteJavafile = remoteSoftdir + javafile;
        remoteZkfile = remoteSoftdir + zkfile;
        cmd = ''
        cmd = cmd + 'tar -zxvf ' + remoteJavafile + ' -C /app && '
        cmd = cmd + 'tar -zxvf ' + remoteZkfile + ' -C /app && '
        cmd = cmd + 'mv  /app/jdk1.8.0_201 /app/jdk && mv  /app/apache-zookeeper-3.5.7-bin /app/zookeeper &&'

        cmd = cmd + "sed -i '/JAVA_HOME=/d' /etc/profile && "
        cmd = cmd + "sed -i '/$JAVA_HOME\/jre/d' /etc/profile && "
        cmd = cmd + "echo 'export JAVA_HOME=/app/jdk '>>/etc/profile && "
        cmd = cmd + "echo 'export CLASSPATH=.:$JAVA_HOME/lib:$JAVA_HOME/jre/lib:$CLASSPATH '>>/etc/profile &&"
        cmd = cmd + "echo 'export PATH=$JAVA_HOME/bin:$JAVA_HOME/jre/bin:$PATH'>>/etc/profile &&"

        cmd = cmd + "sed -i '/ZOOKEEPER_HOME/d' /etc/profile && "
        cmd = cmd + "echo 'export ZOOKEEPER_HOME=/app/zookeeper'>>/etc/profile && "
        cmd = cmd + "echo 'export PATH=$PATH:$ZOOKEEPER_HOME/bin'>>/etc/profile  &&"

        cmd = cmd + 'source /etc/profile'
        print(cmd)
        res = node.call(cmd)
        print(res)

    def startZookeeperServ(self, node):
        cmd = "source /etc/profile && /app/zookeeper/bin/zkServer.sh start"
        res = node.call(cmd)
        print(res)

    def restartZookeeperServ(self, node):
        cmd = 'source /etc/profile && /app/zookeeper/bin/zkServer.sh restart'
        res = node.call(cmd)
        print(res)

    def verifyZookeeperStatus(self, node):
        cmd = 'source /etc/profile && /app/zookeeper/bin/zkServer.sh status'
        res = node.call(cmd)
        print(res)
