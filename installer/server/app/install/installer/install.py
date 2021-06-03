# coding: utf-8

from install.installer.snowball.processer import snowballProcesser
from install.installer.zookeeper.processer import zookeeperProcesser

def Process():
    zookeeperProcesser.install()
    snowballProcesser.install()

