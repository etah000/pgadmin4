# coding: utf-8

#from pgadmin.tools.install.config import snowballConf as conf
from pgadmin.tools.install.installer.node import AbstractNode
from pgadmin.tools.install.installer.common import GetSelfPath
import xmltodict
selfPath = GetSelfPath()

tmpsqlfile = '/app/temp.sql';
class Node(AbstractNode):

    snowballconf = {}
    info = {}
    dbStatus = False

    def __init__(self, name, jsonCfg ):
        self.jsonCfg = jsonCfg;
        infoT = self.getNodeInfo(name,jsonCfg['snowball']['nodes'])
        info = {'name': infoT['name'],
                'host': self.getIP(infoT['ssh'],jsonCfg['hosts']),
                'sshname': infoT['ssh'],
                'tcp_port': infoT['tcp_port'],
                'http_port': infoT['http_port'],
                'interserver_http_port': infoT['interserver_http_port'],
                'timezone':infoT['timezone']}
        #{'name': 'node01', 'host': '192.168.52.128', 'sshname': 'service1', 'tcp_port': '9000', 'http_port': '8123', 'interserver_http_port': '9090'}
        sshT = self.getSSHConf(info['sshname'],jsonCfg['hosts'])
        ssh = {'authMode': '1', 'name': sshT['user'], 'port': sshT['port'], 'passwd': sshT['password'], 'authKeyFile': ''}
        #{'authMode': '1', 'name': 'root', 'port': '22', 'passwd': 'admin', 'authKeyFile': ''}
        self.info = info;
        self.name = name;
        self.host = info['host']
        self.ssh = ssh
        self.snowballconf = self.getSnowballNodeConf(name,jsonCfg['snowball']) #conf.getSnowballNodeConf(name)

    def getSnowballNodeConf(self,name,snowballCfg):
        f = open(selfPath+'/config/snowball.config.xml.tpl', 'r')
        xmlstr = f.read()
        snowballconf = xmltodict.parse(xmlstr)
        #全局设置
        snowballconf['yandex']['path'] = snowballCfg['datadir']
        snowballconf['yandex']['tcp_port'] = snowballCfg['tcp_port']
        snowballconf['yandex']['http_port'] = snowballCfg['http_port']
        snowballconf['yandex']['interserver_http_port'] = snowballCfg['interserver_http_port']
        snowballconf['yandex']['listen_host'] = snowballCfg['listen_host']
        #snowballconf['yandex']['timezone'] = snowballCfg['timezone']
        #集群置空
        snowballconf['yandex']['remote_servers'] = ''
        #局部设置
        for node in snowballCfg['nodes']:
            if node['name'] == name:
                snowballconf['yandex']['path'] = node['path']
                snowballconf['yandex']['tcp_port'] = node['tcp_port']
                snowballconf['yandex']['http_port'] = node['http_port']
                snowballconf['yandex']['interserver_http_port'] = node['interserver_http_port']
                snowballconf['yandex']['listen_host'] = node['listen_host']
                snowballconf['yandex']['timezone'] = node['timezone']
        return  snowballconf
    def getIP(self,name,hosts):
        for host in hosts:
            if host['name'] == name :
                return host['ip']
        return '0.0.0.0'
    #根据名称 节点信息
    def getNodeInfo(self,name,sbnodes):
        for sbnode in sbnodes:
            if sbnode['name'] == name :
                return sbnode
        return {}
    #根据sshname找条目
    def getSSHConf(self,sshname,hosts):
        for host in hosts:
            if host['name'] == sshname :
                return host
        return {}

    def getSnowballConf(self):
        return self.snowballconf


    def query(self,sql):
        cmd = 'snowball-client -h 127.0.0.1 --port '+self.info['tcp_port']+ " --multiquery --query '"+sql+"'";
        res =  self.call(cmd)
        return res.strip()


    def queryByUploadSqlfile(self,sql):
        sqlfile = tmpsqlfile
        self.write(sql, sqlfile);
        cmd = 'snowball-client -h 127.0.0.1 --port ' + self.info['tcp_port'] + " --multiquery < " + tmpsqlfile
        res = self.call(cmd)
        return res

    def checkDbConnect(self):
        if self.dbStatus == True:
            return True

        sql = "select 1;"
        res = self.query(sql);
        if res == '1':
            self.dbStatus = True
            return True
        else:
            self.dbStatus = False
            return False

    def clusterIsExist(self, clustername):
        if self.checkDbConnect() != True:
            return False;

        sql = "select count(1) from system.clusters where cluster = '"+clustername+"';"
        # print(sql)
        res = self.queryByUploadSqlfile(sql).strip()
        res = float(res)
        # print(res)
        if res > 0:
            return True
        else:
            return False

    def createDatabase(self,databasename):
        if self.checkDbConnect() != True:
            return False;
        sql = "create database "+databasename+";"
        res = self.query(sql)
        return res;

    def databaseIsExist(self, databasename):
        if self.checkDbConnect() != True:
            return False;
        sql = " select count(1) from system.databases where name = '"+databasename+"';"
        res = self.queryByUploadSqlfile(sql).strip()
        if res == '1' :
            return True
        else :
            return False
