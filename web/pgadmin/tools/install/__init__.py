
import sys, os, re
import simplejson as json
from flask import url_for, Response, render_template, request, current_app
from flask_babelex import gettext as _
from flask_security import login_required, current_user
from pgadmin.utils import PgAdminModule
from pgadmin.utils import get_storage_directory
import configparser
from pgadmin.utils.ajax import gone
from pgadmin.utils.ajax import make_json_response, \
    make_response as ajax_response, internal_server_error, unauthorized

from pgadmin.utils.driver import get_driver
from pgadmin.utils.menu import MenuItem
from pgadmin.utils.exception import ConnectionLost, SSHTunnelConnectionLost, \
    CryptKeyMissing
from pgadmin.utils.sqlautocomplete.autocomplete import SQLAutoComplete
from flask_babelex import gettext as gettext
from pgadmin.tools.install.installer.snowball.helper import helper
from pgadmin.tools.install.installer.snowball.processer import snowballProcesser
from pgadmin.tools.install.installer.zookeeper.processer import zookeeperProcesser
from pgadmin.tools.install.installer.common import GetSelfPath
from pgadmin.tools.install.installer.common import CheckSSHConnectAndGetOsInfo
selfPath = GetSelfPath()

# 修改为区分大小写
class MyConfigParser(configparser.ConfigParser):

    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr

MODULE_NAME = 'install'
class InstallModule(PgAdminModule):
    LABEL = gettext('Install')
    def get_own_javascripts(self):
        """"
        Returns:
            list: js files used by this module
        """
        return [{
            'name': 'pgadmin.tools.install',
            'path': url_for('static', filename='js/install'),
            'exports': None,
            'when': 'server'
        }]
    def get_own_menuitems(self):
        return {
            'tools': [
                MenuItem(
                    name='mnu_install',
                    priority=999,
                    module="pgAdmin.tools.install",
                    callback='callback_install',
                    icon='fa fa-retweet',
                    label=gettext('Install...')
                )
            ]
        }
    def get_exposed_url_endpoints(self):
        """
        Returns:
            list: URL endpoints for backup module
        """
        return [
            'install.set_install_conf',
            'install.get_install_conf',
            'install.validate_conf'
        ]

blueprint = InstallModule(MODULE_NAME, __name__, static_url_path='/static')


@blueprint.route("/")
@login_required
def index():
    return bad_request(errormsg=_("This URL cannot be called directly."))

@blueprint.route("/install.js")
@login_required
def script():
    """render the import/export javascript file"""
    return Response(
        response=render_template("install/js/install.js", _=_),
        status=200,
        mimetype="application/javascript"
    )

@blueprint.route("/setInstallConf",methods=["GET", "POST"],endpoint="set_install_conf")
def setInstallConf():
    data = json.loads(
        request.data, encoding='utf-8'
    )

    #修改配置文件 conf.zookeeper.install.ini
    zookeepercfgpath = os.path.join(selfPath+"/config/", "conf.zookeeper.install.ini")
    zookeeper = MyConfigParser()
    # 先读出来
    zookeeper.read(zookeepercfgpath, encoding="utf-8")
    # 修改section里面的值
    zookeeper.set("zookeeper", "tickTime", data['config']['zookeeper']['tickTime'])
    zookeeper.set("zookeeper", "initLimit", data['config']['zookeeper']['initLimit'])
    zookeeper.set("zookeeper", "syncLimit", data['config']['zookeeper']['syncLimit'])
    zookeeper.set("zookeeper", "dataDir", data['config']['zookeeper']['dataDir'])
    zookeeper.set("zookeeper", "clientPort", data['config']['zookeeper']['clientPort'])
    #加ssh
    if zookeeper.has_section('sshs'):
        zookeeper.remove_section('sshs')
    zookeeper.add_section('sshs')
    for host in data['config']['hosts']:
        zookeeper.set ('sshs',host['name'],'1,'+host['user']+','+host['password']+','+host['port'])
    #加节点
    if zookeeper.has_section('nodes'):
        zookeeper.remove_section('nodes')
    zookeeper.add_section('nodes')
    for node in data['config']['zookeeper']['nodes']:
        ip = helper.getIP(node['ssh'],data['config']['hosts'])
        zookeeper.set ('nodes',node['name'],node['order']+','+ip+','+node['port1']+','+node['port2'] +','+node['port3'] +','+ node['ssh'])
    zookeeper.write(open(zookeepercfgpath, "r+", encoding="utf-8")) # r+模式

    #修改配置文件 conf.ini
    cfgpath = os.path.join(selfPath+"/config/", "conf.ini")
    conf = MyConfigParser()
    # 先读出来
    conf.read(cfgpath, encoding="utf-8")
    # 修改section里面的值
    conf.set("global", "datadir", data['config']['snowball']['datadir'])
    conf.set("snowballConf", "tcp_port", data['config']['snowball']['tcp_port'])
    conf.set("snowballConf", "http_port", data['config']['snowball']['http_port'])
    conf.set("snowballConf", "interserver_http_port", data['config']['snowball']['interserver_http_port'])
    conf.set("snowballConf", "listen_host", data['config']['snowball']['listen_host'])
    #加节点
    if conf.has_section('nodes'):
        conf.remove_section('nodes')
    conf.add_section('nodes')
    for node in data['config']['snowball']['nodes']:
        ip = helper.getIP(node,data['config']['hosts'])
        conf.set ('nodes',node,ip+','+ node)
    #加ssh
    if conf.has_section('sshs'):
        conf.remove_section('sshs')
    conf.add_section('sshs')
    for host in data['config']['hosts']:
        conf.set ('sshs',host['name'],'1,'+host['user']+','+host['password']+','+host['port'])
    conf.write(open(cfgpath, "r+", encoding="utf-8")) # r+模式
    #安装
    spath=data['config']['general']['path']
    remoteSoftdir=data['config']['general']['remoteSoftdir']
    remoteAppdir=data['config']['general']['remoteAppdir']
    remoteConfDir=data['config']['general']['remoteConfDir']
    zookeeperProcesser.install(spath,remoteSoftdir,remoteAppdir)
    snowballProcesser.install(spath,remoteSoftdir,remoteConfDir)

    res = {
        'code': "0000",
        'msg': "success",
        'data': "install success!"
    }
    return ajax_response(response=res, status=200)

@blueprint.route("/getInstallConf",methods=["GET", "POST"],endpoint="get_install_conf")
def getInstallConf():

    res = {
        'code': "0000",
        'msg': "success",
        'data': data['config']['hosts']
    }
    return ajax_response(response=res, status=200)

@blueprint.route("/validateConf",methods=["GET", "POST"],endpoint="validate_conf")
def getInstallConf():
    data = json.loads(
        request.data, encoding='utf-8'
    )
    res = {
        'code': "0000",
        'msg': "success",
        'data': data['config']['hosts']
    }
    return ajax_response(response=res, status=200)

@blueprint.route("/validateHost",methods=["GET", "POST"],endpoint="validate_host")
def getInstallConf():
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

@blueprint.route('/upload', methods=['POST'])
def upload_part():  # 接收前端上传的一个分片
    size = request.form.get('size')
    chunks = request.form.get('chunks')
    chunk = request.form.get('chunk')
    md5 = request.form.get('md5')
    filename = request.form.get('filename')
    fileHash = request.form.get('fileHash')
    sn = '%s.%s' % (fileHash, chunk)
    file = request.files['file']
    file.save(get_storage_directory()+'/soft/%s' % sn)  # 保存分片到本地

    res = {
        'fileHash': fileHash,
        'chunk': chunk,
        'msg': "success"
    }
    return ajax_response(response=res, status=200)

@blueprint.route('/merge', methods=['POST'])
def upload_success():  # 按序读出分片内容，并写入新文件
    data = json.loads(
        request.data, encoding='utf-8'
    )
    target_filename = data['name']
    fileHash = data['fileHash']
    chunk = 0  # 分片序号
    with open(get_storage_directory()+'/soft/%s' % target_filename, 'wb') as target_file:  # 创建新文件
        while True:
            try:
                filename = get_storage_directory()+'/soft/%s.%s' % (fileHash, chunk)
                source_file = open(filename, 'rb')  # 按序打开每个分片
                target_file.write(source_file.read())  # 读取分片内容写入新文件
                source_file.close()
            except IOError as msg:
                break

            chunk += 1
            os.remove(filename)  # 删除该分片，节约空间
    return ajax_response(response={'code': "0000",'msg': "success"}, status=200)

@blueprint.route('/list', methods=['POST'])
def file_list():
    files = os.listdir(get_storage_directory()+'/soft/')  # 获取文件目录
    #files = list(map(lambda x: x if isinstance(x, str) else x.decode('utf-8'), files) ) # 注意编码
    return ajax_response(response=files, status=200)

@blueprint.route('/download/<filename>', methods=['GET'])
def file_download(filename):
    def send_chunk():  # 流式读取
        store_path = get_storage_directory()+'/soft/%s' % filename
        with open(store_path, 'rb') as target_file:
            while True:
                chunk = target_file.read(20 * 1024 * 1024)
                if not chunk:
                    break
                yield chunk

    return Response(send_chunk(), content_type='application/octet-stream')
