# coding: utf-8
import sys, os, re
# import json
import xmltodict
from pgadmin.tools.install.installer.common import GetSelfPath
from pgadmin.utils import get_storage_directory
from flask import session
# from config import snowballConf as Confobj

selfPath = GetSelfPath()

#softPath = selfPath + '/soft/'

confPath = selfPath + '/config/'

#remoteAppdir = '/app/soft/'

#remoteConfDir = '/etc/snowball-server/'

class AbstractExecutor:

    def geDependencyFile(self,file):
        libs = {
            'openssl':'',
            'openssl-libs': '',
            'libicu':''
        }
        return False


    def prepareDependency(self, node,spath,remoteSoftdir):
        needInstallSoftlist = self.checkDependency(node)
        print(needInstallSoftlist)

        self.uploadDependencyFile(node,needInstallSoftlist,spath,remoteSoftdir)
        self.installDependencyFile(node,needInstallSoftlist,remoteSoftdir)

        return True

    def checkDependency(self, node):
        needInstallSoftlist=[];
        cmd = 'rpm -qa|grep openssl- ; rpm -qa|grep libicu-'
        res = node.call(cmd)
        # print(res)
        if res.find('libicu-') == -1:
            needInstallSoftlist.append('libicu')
        if res.find('openssl-libs-') == -1:
            needInstallSoftlist.append('openssl-libs')
        if res.find('openssl-1') == -1:
            needInstallSoftlist.append('openssl')
        return needInstallSoftlist

    def uploadDependencyFile(self,node, softlist,spath,remoteAppdir):
        node.call('mkdir -p '+remoteAppdir)

        for soft in softlist:
            filename = self.geDependencyFile(soft)
            fullFilename = get_storage_directory()+ spath+ filename
            node.put(fullFilename,remoteAppdir)
        return True

    def installDependencyFile(self,node, softlist,remoteAppdir):
        for soft in softlist:
            filename = self.geDependencyFile(soft)
            cmd = 'rpm -ivh ' + remoteAppdir + filename
            res = node.call(cmd)
            print(res)
        return True


    def prepareFirewalldRule(self, node):
        conf = node.getSnowballConf()
        tcp_port = conf['yandex']['tcp_port']
        http_port = conf['yandex']['http_port']
        interserver_http_port = conf['yandex']['interserver_http_port']

        cmd = 'firewall-cmd --add-port=%s/tcp --permanent;'%(tcp_port)
        cmd = cmd + 'firewall-cmd --add-port=%s/tcp --permanent;'%(http_port)
        cmd = cmd + 'firewall-cmd --add-port=%s/tcp --permanent;'%(interserver_http_port)
        cmd = cmd + 'firewall-cmd --reload'
        res = node.call(cmd)
        print(res)
        # print('check checkFirewalld ...', node)
        return True

    def copyInstallFile(self, node,spath,remoteAppdir,softlist):
        node.call('mkdir -p ' + remoteAppdir)
        for soft, filename in softlist.items():
            fullFilename = get_storage_directory()+ spath+ filename
            node.put(fullFilename, remoteAppdir)
            session['percentagesize'] = session.get('percentagesize')+os.path.getsize(fullFilename)

        return True

    def installSnowballServ(self, node,remoteConfDir):
        print(node.ssh)
        conf = node.getSnowballConf()
        path = conf['yandex']['path']
        node.call('mkdir -p /app ; mkdir -p '+path)

        cmd = 'rpm -qa|grep -i snowball|xargs rpm -e; rpm -ivh /app/soft/snowball-*.rpm;'
        res = node.call(cmd)
        print(res)

        self.updateRomoteConfigXml(node,conf,remoteConfDir)
        #注册license
        res = node.put(get_storage_directory()+'/snowball.license.xml.tpl', remoteConfDir+'config.d/license.xml')
        res = node.call('chown -R snowball:snowball '+path)

    def startSnowballServ(self, node):
        cmd = 'service snowball-server start'
        res = node.call(cmd)
        print(res)

    def restartSnowballServ(self, node):
        cmd = 'service snowball-server restart'
        res = node.call(cmd)
        print(res)

    def verifySnowballStatus(self, node):
        cmd = 'service snowball-server status'
        res = node.call(cmd)
        print(res)

    def replaceLicence(self, node, filename,remoteConfDir):
        res = node.call('cp '+ remoteConfDir +'config.d/license.xml  ' + remoteConfDir +'config.d/license.xml.backup')
        print (res)
        res = node.put(filename, remoteConfDir+'config.d/license.xml')
        print (res)

    def getRemoteConfigXml(self, node,remoteConfDir):
        filename = remoteConfDir+'/config.xml'
        res = node.get(filename)
        return res.strip()

    def updateRomoteConfigXml(self, node, config,remoteConfDir):
        xmlfile = xmltodict.unparse(config, pretty=True);
        filename = remoteConfDir + '/config.xml'
        res = node.write(xmlfile, filename)
        return res
