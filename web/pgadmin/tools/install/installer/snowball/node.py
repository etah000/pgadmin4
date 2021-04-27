# coding: utf-8

from pgadmin.tools.install.config import snowballConf as conf
from pgadmin.tools.install.installer.node import AbstractNode

tmpsqlfile = '/app/temp.sql';
class Node(AbstractNode):

    snowballconf = {}
    info = {}
    dbStatus = False

    def __init__(self, name):
        info = conf.getNodeInfo(name)
        ssh = conf.getSSHConf(info['sshname'])
        self.info = info;
        self.name = name;
        self.host = info['host']
        self.ssh = ssh
        self.snowballconf = conf.getSnowballNodeConf(name)

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
