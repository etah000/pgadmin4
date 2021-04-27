# coding: utf-8

from pgadmin.tools.install.installer.snowball.processer import snowballProcesser
from pgadmin.tools.install.installer.zookeeper.processer import zookeeperProcesser

def Process():
    zookeeperProcesser.install()
    snowballProcesser.install()

