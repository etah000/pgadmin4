# coding: utf-8

import sys
from installer.snowball.license import license
from installer.snowball.cluster import cluster

def mainboard():
    print('请选择功能:')

    print('1. 创建虚拟集群')
    print('2. License更换')
    # print('3. 批量执行SQL(暂未开通)')

    line = sys.stdin.readline()
    line = line.strip()
    if line == 'q':
        isloop = False
    elif line == '1':
        createNewCluster()
    elif line == '2':
        deployLicense()
    elif line == '3':
        batchSqlCall()

def createNewCluster():
    print('createNewCluster')
    cluster.create()
    mainboard()

def deployLicense():
    print('deployLicense')
    license.deploy()
    mainboard()

def batchSqlCall():
    print('batchSqlCall')
    mainboard()

def main():
    mainboard()

main()
