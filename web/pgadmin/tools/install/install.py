# coding: utf-8

import sys
from installer.snowball.processer import snowballProcesser
from installer.zookeeper.processer import zookeeperProcesser
import logging, syslog

def mainboard():
    print('请选择功能:')

    print('1. 安装Zookeeper集群')
    # print('3. 磁盘Raid磁盘')
    print('2. 安装Snowball集群')
    # print('3. 时间同步服务')

    line = sys.stdin.readline()
    line = line.strip()
    if line == 'q':
        isloop = False
    # elif line == '3':
    #     installNtpServer()
    elif line == '1':
        installZookeeper()
    # elif line == '3':
    #     formatDisk()
    elif line == '2':
        installSnowBall()
    # else:
        # installSnowBall()
        # mainboard()
def installSnowBall():
    snowballProcesser.install()
    # mainboard()

def installZookeeper():
    zookeeperProcesser.install()
    mainboard()

def formatDisk():
    print('install formatDisk')
    mainboard()

def installNtpServer():
    print('install ntp server')
    mainboard()

def main():
    mainboard()

main()
