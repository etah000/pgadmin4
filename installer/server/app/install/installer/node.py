import sys, os, re
from install.installer.common import Put, Exec, CheckSSHConnectAndGetOsInfo
from install.installer.common import GetSelfPath
import tempfile

appPath = GetSelfPath()
class AbstractNode():
    name = ''
    host = ''
    ssh = {
        'host':'',
        'authMode':'',
        'name':'',
        'passwd':'',
        'authKeyFile':'',
    }
    os = {
        'name':'',
        'version':''
    }
    status = False
    def write(self, content, filename):
        tmpfd, tempfilename = tempfile.mkstemp()
        #tempfilename = os.path.join(get_storage_directory(),'tempfile')
        with open(tempfilename, "w") as f:
            f.write(str(content))
            f.close()
        self.put(tempfilename, filename)

    def call(self, cmd):
        return Exec(self.host, self.ssh['port'], self.ssh['authMode'], self.ssh['name'], self.ssh['passwd'],self.ssh['authKeyFile'], cmd)

    def put(self,src, dst):
        return Put(self.host, self.ssh['port'], self.ssh['authMode'], self.ssh['name'], self.ssh['passwd'],self.ssh['authKeyFile'], src, dst)

    def get(self, remotefile):
        cmd = 'cat ' + remotefile
        return Exec(self.host, self.ssh['port'], self.ssh['authMode'], self.ssh['name'], self.ssh['passwd'],self.ssh['authKeyFile'], cmd)

    def CheckSSHConnectAndGetOsInfo(self):
        res = CheckSSHConnectAndGetOsInfo(self.host, self.ssh['port'], self.ssh['authMode'], self.ssh['name'],  self.ssh['passwd'], self.ssh['authKeyFile'])
        self.status = res['status']
        self.os['name'] = res['os']
        self.os['version'] = res['osversion']
        return  res['status'];
