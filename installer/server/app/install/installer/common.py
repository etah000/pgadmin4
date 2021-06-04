# coding: utf-8
import sys, os, re
from .ssh_utils import SSHClient

def Put(host, port, authmode, user, password, authfile = '', src = '', dst = ''):
  client = SSHClient(host,user,port,password)
  client.put(src,dst)

def Exec(host,port,authmode,user,password,authfile = '',command = ''):
  client = SSHClient(host,user,port,password)
  client.execute_cmd(command)

def TestSSHConnect(host,port,authmode,user,password,authfile = '',command = ''):
  client = SSHClient(host,user,port,password)
  return client.execute_cmd(command)



def CheckSSHConnectAndGetOsInfo(host,port,authmode, user, password, authfile):
  # print('TestSSHConnectAndGetOsInfo---::command')
  command = 'cat /etc/redhat-release; uname -a'

  exit_status, stdout, stderr = TestSSHConnect(host, port, authmode, user, password, authfile, command)
  res = stdout.read().decode()


  os = 'unkown'
  v = 'unkown'
  if (res != False):
    connectStatus = True
    res = res.replace('\r\n', '').strip()
    if (res.find('CentOS') != -1):
      os = 'centos'
    elif (res.find('Red Hat') != -1):
      os = 'redhat'
    elif (res.find('Ubuntu') != -1):
      os = 'ubuntu'
    else:
      os = 'unkown'

    if os == 'centos' or os == 'redhat':
      r = re.findall('release (.+?) \(', res)
      v = r[0][0:3]
    elif os == 'ubuntu':
      r = re.findall('~(.+?)-', res)
      v = r[0][0:5]
    else:
      v = 'unkown'
    if (res.find('refused')!=-1) :
        connectStatus = False

  else:
    connectStatus = False
  res = {
    'os':os,
    'osversion' :v,
    'status' :connectStatus
  }
  return res;

def GetSelfPath():
  selfpath = os.path.dirname(os.path.abspath(__file__))
  return os.path.dirname(selfpath)