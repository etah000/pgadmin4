# coding: utf-8

from  pgadmin.tools.install.installer.snowball.executor.abstract import AbstractExecutor

class Cent7Executor(AbstractExecutor):
    def geDependencyFile(self,file):
        libs = {
            'openssl-libs':'openssl-libs-1.0.2k-19.el7.x86_64.rpm',
            'openssl':'openssl-1.0.2k-19.el7.x86_64.rpm',
            'libicu':'libicu-50.2-3.el7.x86_64.rpm'
        }
        if libs.has_key(file):
            return libs[file]
        return False

    def getSnowballFile(self):
        return {
            'common':'snowball-common-static-2.8.13-2.el7.x86_64.rpm',
            'server':'snowball-server-2.8.13-2.el7.x86_64.rpm',
            'client':'snowball-client-2.8.13-2.el7.x86_64.rpm',
        }
    pass

