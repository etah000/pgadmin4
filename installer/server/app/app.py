import os
import simplejson as json
from flask import request, current_app,  Flask, flash
from flask_cors import CORS
from ajax import make_response as ajax_response
from install.installer.common import CheckSSHConnectAndGetOsInfo
from install.installer.snowball.processer import Processer as SnowballProcesser
from install.installer.zookeeper.processer import Processer as ZookeeperProcesser
import global_vars

app = Flask(__name__)
app.secret_key = os.urandom(16)
CORS(app, supports_credentials=True) # Awllow CORS
@app.route("/install/validateHost",methods=["GET", "POST"])
def validateHost():
    data = json.loads(
        request.data, encoding='utf-8'
    )
    outdata = []
    for host in data['hosts']:
        checkres = CheckSSHConnectAndGetOsInfo(host['ip'], host['port'], '1', host['user'],  host['password'], '')
        checkres.update({
            'name': host['name']
        })
        outdata.append(checkres)
    res = {
        'code': "0000",
        'msg': "success",
        'data': outdata
    }
    return ajax_response(response=res, status=200)
@app.route("/install/setInstallConf",methods=["GET", "POST"])
def setInstallConf():
    data = json.loads(
        request.data, encoding='utf-8'
    )
    res = {
        'code': "0000",
        'msg': "success",
        'data': "install success!"
    }
    #要处理的文件大小
    allsize = 0
    global_vars.session['percentagesize'] = 0

    #zookeeperselected
    if data['config']['zookeeperselected'] == True:
        nodeCount =  len(data['config']['zookeeper']['nodes'])
        zookeeperpath = data['config']['zookeeper']['softlist']['zookeeper']
        allsize += os.path.getsize(zookeeperpath)*nodeCount
        jdkpath = data['config']['zookeeper']['softlist']['jdk']
        allsize += os.path.getsize(jdkpath)*nodeCount

    if data['config']['snowballselected'] == True:
        nodeCount =  len(data['config']['snowball']['nodes'])
        commonpath = data['config']['snowball']['softlist']['common']
        allsize += os.path.getsize(commonpath)*nodeCount
        serverpath = data['config']['snowball']['softlist']['server']
        allsize += os.path.getsize(serverpath)*nodeCount
        clientpath =data['config']['snowball']['softlist']['client']
        allsize += os.path.getsize(clientpath)*nodeCount
    global_vars.session['allsize'] = allsize

    #安装
    spath=data['config']['general']['path']
    remoteSoftdir=data['config']['general']['remoteSoftdir']
    remoteAppdir=data['config']['general']['remoteAppdir']
    remoteConfDir=data['config']['general']['remoteConfDir']
    try:
        #zookeeperselected
        if data['config']['zookeeperselected'] == True:
            zksoftlist=data['config']['zookeeper']['softlist']
            zknodes = []
            for node in data['config']['zookeeper']['nodes']:
                zknodes.append(node['name'])
            current_app.logger.info('install  Zookeeper start')
            ZookeeperProcesser().install(spath,remoteSoftdir,remoteAppdir,zksoftlist,zknodes,data['config'])
            current_app.logger.info('install  Zookeeper end')
            flash(message="50", category="test")
        #snowballselected
        if data['config']['snowballselected'] == True:
            sbsoftlist=data['config']['snowball']['softlist']
            sbnodes = []
            for node in data['config']['snowball']['nodes']:
                sbnodes.append(node['name'])
            current_app.logger.info('install  Snowball start')
            SnowballProcesser().install(spath,remoteSoftdir,remoteConfDir,sbsoftlist,sbnodes,data['config'])
            current_app.logger.info('install  Snowball end')
    except Exception as e:
        print(e)
        res = {
            'code': "9999",
            'msg': "server error",
            'data': ""
        }
        return ajax_response(response=res, status=200)
    return ajax_response(response=res, status=200)
@app.route('/install/processer', methods=["GET", "POST"])
def processer():
    data ={'percentage': 100*global_vars.session.get('percentagesize')*0.9/global_vars.session.get('allsize')}
    return ajax_response(response={'code': "0000",'msg': "success",'data': data}, status=200)

app.run(port=5000, debug=True)
