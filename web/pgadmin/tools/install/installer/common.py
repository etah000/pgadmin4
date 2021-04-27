# coding: utf-8

import sys, os, re
import pexpect

def Put(host, port, authmode, user, password, authfile = '', src = '', dst = ''):
  if(authmode == 'rsaauth'):
    idfile = '-i %s'%(authfile)
  else:
    idfile = ''
  # print('copy local file : %s ==> %s:%s'%(src,host,dst))
  cmd = 'scp %s -r -P %s %s %s@%s:%s' %(idfile,port,src,user,host,dst);
  child=pexpect.spawn(cmd, timeout=600)
  o=''
  try:
    if(authmode == 'rsaauth'):
      pass
    else:
      i=child.expect(['password:','continue connecting (yes/no)?'])
      if i == 1:
        child.sendline('yes')
        i=child.expect(['password:'])
      if i==0:
        child.sendline(password)

  except pexpect.EOF:
    child.close()
  else:
    o=child.read()
    child.expect(pexpect.EOF)
    child.close()
  return o.decode()



def Exec(host,port,authmode,user,password,authfile = '',command = ''):

  if(authmode == 'rsaauth'):
    idfile = '-i %s'%(authfile)
  else:
    idfile = ''
  cmd = 'ssh %s -p%s %s@%s "%s"' %(idfile, port,user,host,command)

  # print(cmd)
  child=pexpect.spawn(cmd, timeout=60)
  o=''
  try:

    if (authmode == 'rsaauth'):
      pass
    else:
      # First connect
      i=child.expect(['password:','continue connecting (yes/no)?'])
      if i == 1:
        child.sendline('yes')
        i=child.expect(['password:'])

      if i==0:
        child.sendline(password)

  except Exception as e :
    print(e)
  except pexpect.EOF:
    child.close()
  else:
    o=child.read()
    child.expect(pexpect.EOF)
    child.close()
  return o.decode()

def TestSSHConnect(host,port,authmode,user,password,authfile = '',command = ''):
  if (authmode == 'rsaauth'):
    idfile = '-i %s' % (authfile)
  else:
    idfile = ''
  cmd = 'ssh %s -p%s %s@%s "%s"' % (idfile, port, user, host, command)
  # print(cmd)
  # sys.stdout.write(host)
  child = pexpect.spawn(cmd)
  o = ''
  try:
    try:
      i = child.expect(['password:','continue connecting (yes/no)?','No route to host','Permission denied'])
      if i==1:
        child.sendline('yes')
        if (authmode != 'rsaauth'):
          i = child.expect(['password:'])
          child.sendline(password)
      elif i==0:
        child.sendline(password)
      elif i == 2:
        sys.stdout.write(' ERROR: No route to host')
        return False
      elif i == 3:
        sys.stdout.write(' ERROR: Permission denied')
        return False
      else:
        sys.stdout.write(' ERROR: Unknow ERROR')
        return False

    except pexpect.EOF as e:
        o = pexpect.run(cmd)
        child.close()
        return o.decode()
  except Exception as e :
    # raise e
    return  False;
  except pexpect.EOF as e:
    child.close()
    raise e
    return False;
  else:
    o=child.read()
    child.expect(pexpect.EOF)
    child.close()
  return o.decode()


def CheckSSHConnectAndGetOsInfo(host,port,authmode, user, password, authfile):
  # print('TestSSHConnectAndGetOsInfo---::command')
  command = 'cat /etc/redhat-release; uname -a'

  res = TestSSHConnect(host, port, authmode, user, password, authfile, command)

  os = 'unkown'
  v = 'unkown'
  if (res != False):
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
    connectStatus = True
  else:
    connectStatus = False
  res = {
    'os':os,
    'osversion' :v,
    'status' :connectStatus
  }
  return res;

#
# def Confirm(msg):
#   isloop = True
#   result =  False
#   while isloop:
#     # sys.stdout.write(msg)
#     sys.stdout.write(msg + ' (y/n) ')
#     line = sys.stdin.readline()
#     line = line.strip()
#     if line == 'y' or line == 'yes':
#       isloop = False
#       result = True
#     elif line == 'n' or line == 'no':
#       isloop = False
#       result = False
#     else:
#       # sys.stdout.write(line)
#       # print(line)
#       pass
#
#   return result
#
# def Option(options):
#   for option in options:
#     continue
#
#
# def Alert(msg):
#   print(msg)
#   sys.stdout.write('Press any key to contine, Ctrl+c to Cancel ')
#   line = sys.stdin.readline()
#   return line

#
# def Input(msg):
#   return True

def GetSelfPath():
  selfpath = os.path.dirname(os.path.abspath(__file__))
  return os.path.dirname(selfpath)
