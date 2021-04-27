# coding: utf-8

from  pgadmin.tools.install.installer.zookeeper.executor.abstract import AbstractExecutor

class Cent7Executor(AbstractExecutor):

    def getZookeeperFile(self):
        return {
            'zookeeper':'apache-zookeeper-3.5.7-bin.tar.gz',
            'jdk':'jdk-8u201-linux-x64.tar.gz'
        }
    pass

