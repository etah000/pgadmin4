# coding: utf-8
from installer.common import GetSelfPath
import urllib2
import os


path = GetSelfPath()

filelist = [
    'libicu-50.2-3.el7.x86_64.rpm',
    'openssl-1.0.2k-19.el7.x86_64.rpm',
    'openssl-libs-1.0.2k-19.el7.x86_64.rpm',
    'snowball-client-2.8.13-2.el7.x86_64.rpm',
    'snowball-common-static-2.8.13-2.el7.x86_64.rpm',
    'snowball-server-2.8.13-2.el7.x86_64.rpm',
    'apache-zookeeper-3.5.7-bin.tar.gz',
    'jdk-8u201-linux-x64.tar.gz',
    'grafana-6.5.2-1.x86_64.rpm',
    'grafana-piechart-panel.zip',
    'prometheus-2.14.0-1.el7.x86_64.rpm',
    'node_exporter-0.18.1-6.el7.x86_64.rpm',
    'snowball_exporter-0.13.1-6.el7.x86_64.rpm',
    'process-exporter-0.6.0-1.el7.x86_64.rpm',

    'ntpdate-4.2.6p5-29.el7.centos.x86_64.rpm',


    'fontpackages-filesystem-1.44-8.el7.noarch.rpm',
    'dejavu-fonts-common-2.33-6.el7.noarch.rpm',
    'dejavu-sans-fonts-2.33-6.el7.noarch.rpm',
    'fontconfig-2.13.0-4.3.el7.x86_64.rpm',

    'xorg-x11-font-utils-7.5-21.el7.x86_64.rpm',
    'libfontenc-1.1.3-3.el7.x86_64.rpm',
    'urw-fonts-2.4-16.el7.noarch.rpm'
]
downloadurl = 'https://inforefiner.oss-cn-beijing.aliyuncs.com/soft/'
localsoftdir  =  path + '/soft/';

localfileList = os.listdir(localsoftdir)

def checkSoftIsexist(filename):
    isExist = False;
    for i in localfileList:
        if filename == i :
            isExist = True
            break;
    return isExist;

def Download():
    for softname in filelist:
        if checkSoftIsexist(softname) == True:
            print('Existed:' + softname)
            continue;
        else:
            print('Download:' + softname)
            remotefilename = downloadurl + softname
            localfilename = localsoftdir + softname
            f = urllib2.urlopen(remotefilename)
            data = f.read()
            with open (localfilename,'wb') as temp:
                temp.write(data)

Download();
