<template>
  <a id="install" href="#" data-toggle="pg-menu" role="menuitem" class="dropdown-item">
    <span data-test="menu-item-text"  @click="dialogFormVisible = true">{{ gettext('Install') }} </span>
    <el-dialog width="65%"
               :modal="true"
               :close-on-click-modal="false"
               :append-to-body=true
               :modal-append-to-body=true
               :visible.sync="dialogFormVisible">
        <form-wizard @on-complete="onComplete"
                     @on-validate="handleValidation"
                     @on-loading="setLoading"
                     @on-error="handleErrorMessage"
                     title="安装向导"
                     back-button-text="上一步"
                     next-button-text="下一步"
                     finish-button-text="开始安装"
                     shape="circle"
                     color="#20a0ff"
                     error-color="#fa0202">
          <!--<tab-content title="软件源" icon="el-icon-coin" :before-change="validateSource" >
            <el-form :model="general"  ref="generalForm" :rules="rulesGeneral"  size="medium">
              <el-form-item label="软件包准备" label-width="110px" prop="path">
                         <el-input v-model="general.path" autocomplete="off"></el-input>
                             <el-button @click="fileSelectionDlg" size="medium" icon="el-icon-circle-plus-outline" type="primary" round>选取
                             </el-button>

              </el-form-item>
            </el-form>
          </tab-content>-->
          <tab-content title="组件选择" icon="el-icon-coin" :before-change="validatePgk" >
            <el-collapse>
              <el-collapse-item  name="1">
                <template slot="title">
                  <el-checkbox v-model="zookeeperselected">zookeeper service </el-checkbox>
                </template>
                <el-form  size="medium" label-width="180px">
                  <el-form-item label="apache-zookeeper"  prop="zookeeper">
                    <el-input v-model="zookeeper.softlist.zookeeper" :readonly="true" >
                      <template slot="append">
                        <yl-upload
                            action="/install/upload"
                            :data="chunkData"
                            :on-success="handleSuccess"
                            :before-upload="beforeZookeeperUpload"
                            :show-file-list = false
                             accept = ".gz, .zip,.bz2, .rpm"
                            :chunk-size="1024 * 1024 * 3"
                            :thread="4"
                        >
                          <i class="el-icon-upload"></i>
                        </yl-upload>
                      </template>
                    </el-input>
                  </el-form-item>
                  <el-form-item label="jdk"  prop="jdk">
                    <el-input v-model="zookeeper.softlist.jdk" :readonly="true" >
                      <template slot="append">
                        <yl-upload
                            action="/install/upload"
                            :data="chunkData"
                            :on-success="handleSuccess"
                            :before-upload="beforeJdkUpload"
                            :show-file-list = false
                            accept = ".gz, .zip,.bz2, .rpm"
                            :chunk-size="1024 * 1024 * 3"
                            :thread="4"
                        >
                          <i class="el-icon-upload"></i>
                        </yl-upload>
                      </template>
                    </el-input>
                  </el-form-item>
                </el-form>
              </el-collapse-item>
              <el-collapse-item  name="2">
                <template slot="title">
                  <el-checkbox v-model="snowballselected">snowball db </el-checkbox>
                </template>
                <el-form  size="medium" label-width="180px">
                  <el-form-item label="snowball-common"  prop="common">
                    <el-input v-model="snowball.softlist.common" :readonly="true">
                      <template slot="append">
                        <yl-upload
                            action="/install/upload"
                            :data="chunkData"
                            :on-success="handleSuccess"
                            :before-upload="beforeSnowballCommonUpload"
                            :show-file-list = false
                            accept = ".gz, .zip,.bz2, .rpm"
                            :chunk-size="1024 * 1024 * 3"
                            :thread="4"
                        >
                          <i class="el-icon-upload"></i>
                        </yl-upload>
                      </template>
                    </el-input>
                  </el-form-item>
                  <el-form-item label="snowball-server"  prop="server">
                    <el-input v-model="snowball.softlist.server" :readonly="true">
                      <template slot="append">
                        <yl-upload
                            action="/install/upload"
                            :data="chunkData"
                            :on-success="handleSuccess"
                            :before-upload="beforeSnowballServerUpload"
                            :show-file-list = false
                            accept = ".gz, .zip,.bz2, .rpm"
                            :chunk-size="1024 * 1024 * 3"
                            :thread="4"
                        >
                          <i class="el-icon-upload"></i>
                        </yl-upload>
                      </template>
                    </el-input>
                  </el-form-item>
                  <el-form-item label="snowball-client"  prop="client">
                    <el-input v-model="snowball.softlist.client" :readonly="true">
                      <template slot="append">
                        <yl-upload
                            action="/install/upload"
                            :data="chunkData"
                            :on-success="handleSuccess"
                            :before-upload="beforeSnowballClientUpload"
                            :show-file-list = false
                            accept = ".gz, .zip,.bz2, .rpm"
                            :chunk-size="1024 * 1024 * 3"
                            :thread="4"
                        >
                          <i class="el-icon-upload"></i>
                        </yl-upload>
                      </template>
                    </el-input>
                  </el-form-item>
                </el-form>
              </el-collapse-item>
            </el-collapse>
          </tab-content>
          <tab-content title="服务器设置" icon="el-icon-set-up" :before-change="validateHost" >
            <el-button @click="add" size="medium" icon="el-icon-circle-plus-outline" type="primary" round>添加服务器
            </el-button>
            <el-table
                :data="hosts"
                style="width: 100%">
              <el-table-column
                  prop="name"
                  label="服务器名"
                  >
                <template slot-scope="scope">
                  <el-input  size="small" v-model="scope.row.name" ></el-input>
                </template>
              </el-table-column>
              <el-table-column
                  prop="ip"
                  label="ip地址"
                  width = "240"
                  >
                <template slot-scope="scope">
                  <ip :index="scope.$index" :ip="scope.row.ip"  @change="handleChange"></ip>
                </template>
              </el-table-column>
              <el-table-column
                  prop="port"
                  label="ssh端口"
              >
                <template slot-scope="scope">
                  <el-input  size="small" v-model="scope.row.port" ></el-input>
                </template>
              </el-table-column>
              <el-table-column
                  prop="user"
                  label="用户名"
                  >
                <template slot-scope="scope">
                  <el-input  size="small" v-model="scope.row.user"></el-input>
                </template>
              </el-table-column>
              <el-table-column
                  prop="password"
                  label="密码"
                  >
                <template slot-scope="scope">
                  <el-input type="password"  size="small" v-model="scope.row.password"></el-input>
                </template>
              </el-table-column>
              <el-table-column
                  label="操作"
                  >
                <template slot-scope="scope">
                  <el-button
                      @click.stop.prevent="deleteRow(scope.$index, hosts)"
                      size="small"
                      type="danger"
                  >
                    移除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </tab-content>
          <tab-content title="服务设置" icon="el-icon-setting" :before-change="validateService">
            <el-collapse>
              <el-collapse-item title="zookeeper service 设置" v-if="zookeeperselected" name="1">
                <el-form :model="zookeeper" ref="zookeeperForm" :rules="rulesZk" size="medium">
                  <el-row>
                    <el-col :span="12">
                      <el-form-item label="tickTime" :label-width="formLabelWidth" prop="tickTime">
                        <el-input v-model="zookeeper.tickTime" autocomplete="off"></el-input>
                      </el-form-item>
                      <el-form-item label="initLimit" :label-width="formLabelWidth" prop="initLimit">
                        <el-input v-model="zookeeper.initLimit" autocomplete="off"></el-input>
                      </el-form-item>
                      <el-form-item label="syncLimit" :label-width="formLabelWidth" prop="syncLimit">
                        <el-input v-model="zookeeper.syncLimit" autocomplete="off"></el-input>
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="dataDir" :label-width="formLabelWidth" prop="dataDir">
                        <el-input v-model="zookeeper.dataDir" autocomplete="off"></el-input>
                      </el-form-item>
                      <el-form-item label="clientPort" :label-width="formLabelWidth" prop="clientPort">
                        <el-input v-model="zookeeper.clientPort" autocomplete="off"></el-input>
                      </el-form-item>
                    </el-col>
                  </el-row>
                  <el-row>
                    <el-col :span="24">
                      <el-button @click="addzk" size="medium" icon="el-icon-circle-plus-outline" type="primary" round>添加zookeeper节点</el-button>
                      <el-table
                          :data="zookeeper.nodes"
                          style="width: 100%">
                        <el-table-column prop="order" label="序列" >
                          <template slot-scope="scope">
                            <el-input  size="small" v-model="scope.row.order"></el-input>
                          </template>
                        </el-table-column>
                        <el-table-column prop="name" label="zk节点名" >
                          <template slot-scope="scope">
                            <el-input  size="small" v-model="scope.row.name"></el-input>
                          </template>
                        </el-table-column>
                        <el-table-column prop="ssh" label="所在服务器" width="120">
                          <template slot-scope="scope">
                            <el-select
                                v-model="scope.row.ssh"
                                size="small"
                                filterable
                                allow-create
                                default-first-option
                            >
                              <el-option
                                  v-for="item in hosts"
                                  :key="item.name"
                                  :label="item.name"
                                  :value="item.name">
                              </el-option>
                            </el-select>
                          </template>
                        </el-table-column>
                        <el-table-column prop="port1" label="客户端连接端口" width="120" >
                          <template slot-scope="scope">
                            <el-input  size="small" v-model="scope.row.port1"></el-input>
                          </template>
                        </el-table-column>
                        <el-table-column prop="port2" label="心跳端口"  >
                          <template slot-scope="scope">
                            <el-input  size="small" v-model="scope.row.port2"></el-input>
                          </template>
                        </el-table-column>
                        <el-table-column prop="port3" label="集群内通讯端口" width="120">
                          <template slot-scope="scope">
                            <el-input  size="small" v-model="scope.row.port3"></el-input>
                          </template>
                        </el-table-column>

                        <el-table-column label="操作" >
                          <template slot-scope="scope">
                            <el-button @click.stop.prevent="deleteRowZk(scope.$index, zookeeper.nodes)" size="small" type="danger">
                              移除
                            </el-button>
                          </template>
                        </el-table-column>
                      </el-table>
                    </el-col>
                  </el-row>
                </el-form>
              </el-collapse-item>
              <el-collapse-item title="snowball db 设置" v-if="snowballselected" name="2">
                <el-form :model="snowball" ref="snowballForm" :rules="rulesSnowball"  size="medium">
                  <el-row>
                    <el-col :span="12">
                      <el-form-item label="datadir" :label-width="formLabelWidth" prop="datadir">
                        <el-input v-model="snowball.datadir" autocomplete="off"></el-input>
                      </el-form-item>
                      <el-form-item label="tcp_port" :label-width="formLabelWidth" prop="tcp_port">
                        <el-input v-model="snowball.tcp_port" autocomplete="off"></el-input>
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="http_port" :label-width="formLabelWidth" prop="http_port">
                        <el-input v-model="snowball.http_port" autocomplete="off"></el-input>
                      </el-form-item>
                      <el-form-item label="listen_host" :label-width="formLabelWidth" prop="listen_host">
                        <ip  :index=0 :ip="snowball.listen_host" @change="handleChangeSb"></ip>
                      </el-form-item>
                    </el-col>
                  </el-row>
                  <el-row>
                    <el-col :span="12">
                      <el-form-item label="interserver_http_port" label-width="160px" prop="interserver_http_port">
                        <el-input v-model="snowball.interserver_http_port" autocomplete="off"></el-input>
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="timezone" :label-width="formLabelWidth" prop="timezone">
                        <el-input v-model="snowball.timezone" autocomplete="off"></el-input>
                      </el-form-item>
                    </el-col>
                  </el-row>
                  <el-row>
                    <el-col :span="24">
                      <el-form-item label="license" :label-width="formLabelWidth"  prop="licensetpl">
                        <el-input v-model="snowball.licensetpl" :readonly="true" >
                          <template slot="append">
                            <yl-upload
                                action="/install/upload"
                                :data="chunkData"
                                :on-success="handleSuccess"
                                :before-upload="beforeLicensetplUpload"
                                :show-file-list = false
                                accept = ".xml, .tpl"
                                :chunk-size="1024 * 1024 * 3"
                                :thread="4"
                            >
                              <i class="el-icon-upload"></i>
                            </yl-upload>
                          </template>
                        </el-input>
                      </el-form-item>
                    </el-col>
                  </el-row>
                  <el-row>
                    <el-col :span="24">
                      <el-button @click="addsb" size="medium" icon="el-icon-circle-plus-outline" type="primary" round>添加snowball节点</el-button>
                      <el-table
                          :data="snowball.nodes"
                          style="width: 100%">
                        <el-table-column prop="name" fixed label="snowball节点名" width="120">
                          <template slot-scope="scope">
                            <el-input  size="small" v-model="scope.row.name"></el-input>
                          </template>
                        </el-table-column>
                        <el-table-column prop="ssh" label="所在服务器" width="120">
                          <template slot-scope="scope">
                            <el-select
                                v-model="scope.row.ssh"
                                size="small"
                                filterable
                                allow-create
                                default-first-option
                            >
                              <el-option
                                  v-for="item in hosts"
                                  :key="item.name"
                                  :label="item.name"
                                  :value="item.name">
                              </el-option>
                            </el-select>
                          </template>
                        </el-table-column>
                        <el-table-column prop="path" label="数据路径" width="150" >
                          <template slot-scope="scope">
                            <el-input  size="small" v-model="scope.row.path"></el-input>
                          </template>
                        </el-table-column>
                        <el-table-column prop="tcp_port" label="tcp_port" width="80" >
                          <template slot-scope="scope">
                            <el-input  size="small" v-model="scope.row.tcp_port"></el-input>
                          </template>
                        </el-table-column>
                        <el-table-column prop="http_port" label="http_port" width="80" >
                          <template slot-scope="scope">
                            <el-input  size="small" v-model="scope.row.http_port"></el-input>
                          </template>
                        </el-table-column>
                        <el-table-column prop="interserver_http_port" label="interserver_http_port" width="100">
                          <template slot-scope="scope">
                            <el-input  size="small" v-model="scope.row.interserver_http_port"></el-input>
                          </template>
                        </el-table-column>
                        <el-table-column prop="listen_host" label="listen_host" width="200" >
                          <template slot-scope="scope">
                            <ip :index="scope.$index" :ip="scope.row.listen_host"  @change="handleChangeSblisten"></ip>
                          </template>
                        </el-table-column>
                        <el-table-column prop="timezone" label="timezone" width="150">
                          <template slot-scope="scope">
                            <el-input  size="small" v-model="scope.row.timezone"></el-input>
                          </template>
                        </el-table-column>

                        <el-table-column label="操作" >
                          <template slot-scope="scope">
                            <el-button @click.stop.prevent="deleteRowSb(scope.$index, snowball.nodes)" size="small" type="danger">
                              移除
                            </el-button>
                          </template>
                        </el-table-column>
                      </el-table>
                    </el-col>
                  </el-row>
                </el-form>
              </el-collapse-item>
            </el-collapse>
          </tab-content>
          <tab-content title="安装" icon="el-icon-monitor">
            <el-progress :text-inside="true" :stroke-width="26" :percentage="percentage"></el-progress>
            <el-alert
                v-show="installres"
                type="success"
                :description=res
                show-icon>
            </el-alert>
          </tab-content>
          <div class="loader" v-if="loadingWizard"></div>
          <div v-if="errorMsg">
            <span class="error">{{errorMsg}}</span>
          </div>
        </form-wizard>
    </el-dialog>
  </a>
</template>
<script>
import {getInstallConf, setInstallConf,validateConf,validateHost,merge,list,processer} from 'top/static/js/api/install.js'
import YlUpload from 'top/misc/upload/index.vue'
import Ip from 'top/tools/install/static/js/components/ip.vue';
import gettext from 'sources/gettext'
import {Message} from "element-ui";

export default {
  components: {
    Ip,
    YlUpload
  },
  name: 'install',
  data: function () {
    return {
      zookeeperselected: false,
      snowballselected: false,
      multipleSelection: [],
      loadingWizard: false,
      errorMsg: null,
      count: 0,
      ip: '127.0.0.1', // or null
      port: '8888', // or null
      percentage:0,
      num:0,
      finalModel: {},
      activeTabIndex: 0,
      active: 0,
      res: '',
      installres: false,
      dialogFormVisible: false,
      formLabelWidth: '90px',
      general:{
        path:'/',
        remoteSoftdir:'/app/soft/',
        remoteAppdir:'/app/zookeeper/',
        remoteConfDir:'/etc/snowball-server/',
        remoteJdkdir:'/app/jdk/'
      },
      hosts: [
        {name: 'server1', ip: '192.168.52.128', user: 'root', password: 'admin', port: '22', status: 1},
        {name: 'server2', ip: '192.168.52.129', user: 'root', password: 'admin', port: '22', status: 1},
        {name: 'server3', ip: '192.168.52.130', user: 'root', password: 'admin', port: '22', status: 1}
      ],
      zookeeper: {
        softlist:{
          'zookeeper':'',
          'jdk':''},
        tickTime: '2000',
        initLimit: '10',
        syncLimit: '5',
        dataDir: '/data/zookeeper',
        clientPort: '2181',
        nodes: [
          {name: 'zk001', order: '1', port1: '2181', port2: '2888', port3: '3888', ssh: 'server1'},
          {name: 'zk002', order: '2', port1: '2181', port2: '2888', port3: '3888', ssh: 'server2'},
          {name: 'zk003', order: '3', port1: '2181', port2: '2888', port3: '3888', ssh: 'server3'}
        ]
      },
      snowball: {
        softlist:{
          'common':'',
          'server':'',
          'client':''},
        datadir: '/data',
        tcp_port: '9000',
        http_port: '8123',
        interserver_http_port: '9090',
        listen_host: '0.0.0.0',
        timezone:'Asia/Shanghai',
        basecfgtpl:'snowball.config.xml.tpl',
        licensetpl:'',
        nodes: [
          {name: 'node01', path:'/data/snowball/',tcp_port:'9000',http_port:'8123',interserver_http_port:'9090',listen_host:'0.0.0.0',timezone:'Asia/Shanghai', ssh: 'server1'},
          {name: 'node02', path:'/data/snowball/',tcp_port:'9000',http_port:'8123',interserver_http_port:'9090',listen_host:'0.0.0.0',timezone:'Asia/Shanghai', ssh: 'server2'},
          {name: 'node03', path:'/data/snowball/',tcp_port:'9000',http_port:'8123',interserver_http_port:'9090',listen_host:'0.0.0.0',timezone:'Asia/Shanghai', ssh: 'server3'}
        ]
      },
      rulesGeneral:{
        path: [
          {required: true, message: '不能为空', trigger: 'blur'}
        ]
      },
      rulesZk: {
        tickTime: [
          {required: true, message: '不能为空', trigger: 'blur'}
        ],
        initLimit: [
          {required: true, message: '不能为空', trigger: 'blur'}
        ],
        syncLimit: [
          {required: true, message: '不能为空', trigger: 'blur'}
        ],
        dataDir: [
          {required: true, message: '不能为空', trigger: 'blur'}
        ],
        clientPort: [
          {required: true, message: '不能为空', trigger: 'blur'}
        ]
      },
      rulesSnowball: {
        datadir: [
          {required: true, message: '不能为空', trigger: 'blur'}
        ],
        timezone: [
          {required: true, message: '不能为空', trigger: 'blur'}
        ],
        licensetpl: [
          {required: true, message: '不能为空', trigger: 'blur'}
        ],
        tcp_port: [
          {required: true, message: '不能为空', trigger: 'blur'}
        ],
        http_port: [
          {required: true, message: '不能为空', trigger: 'blur'}
        ],
        interserver_http_port: [
          {required: true, message: '不能为空', trigger: 'blur'}
        ],
        listen_host: [
          {required: true, message: '不能为空', trigger: 'blur'}
        ],
        nodes: [
          {required: true, message: '不能为空', trigger: 'blur'}
        ]
      },
    }
  },
  created() {
  },
  mounted() {
    /*getInstallConf().then(response => {
      //const { data } = response
      //this.countData = data
    }).catch(() => {
    })*/
  },
  methods: {
    gettext: function (text) {
      return gettext(text);
    },
    beforeLicensetplUpload(file){
      if(file.name.indexOf('license')==-1){
        this.$message.error('选择的 license 安装文件有误，请重新选择！');
        return false
      }else {
        this.snowball.licensetpl = file.name
        return true
      }
    },
    beforeZookeeperUpload(file){
      if(file.name.indexOf('apache-zookeeper')==-1){
        this.$message.error('选择的 apache-zookeeper 安装文件有误，请重新选择！');
        return false
      }else {
        this.zookeeper.softlist.zookeeper = file.name
        return true
      }
    },
    beforeJdkUpload(file){
      if(file.name.indexOf('jdk')==-1){
        this.$message.error('选择的 jdk 安装文件有误，请重新选择！');
        return false
      }else {
        this.zookeeper.softlist.jdk = file.name
        return true
      }
    },
    beforeSnowballCommonUpload(file){
      if(file.name.indexOf('snowball-common')==-1){
        this.$message.error('选择的 snowball-common 安装文件有误，请重新选择！');
        return false
      }else {
        this.snowball.softlist.common = file.name
        return true
      }
    },
    beforeSnowballClientUpload(file){
      if(file.name.indexOf('snowball-client')==-1){
        this.$message.error('选择的 snowball-client 安装文件有误，请重新选择！');
        return false
      }else {
        this.snowball.softlist.client = file.name
        return true
      }
    },
    beforeSnowballServerUpload(file){
      if(file.name.indexOf('snowball-server')==-1){
        this.$message.error('选择的 snowball-server 安装文件有误，请重新选择！');
        return false
      }else {
        this.snowball.softlist.server = file.name
        return true
      }
    },
    chunkData(option){
      return{
        size: option.fileSize, // 总文件大小
        chunks: option.chunkTotal, // 所有切片数量
        chunk: option.chunkIndex,// 当前切片下标
        md5: option.chunkHash, // 单个切片hash
        filename: option.fileName, // 文件名
        fileHash: option.fileHash, // 整个文件hash
        chunkSize: option.chunkSize // 整个文件hash
      }
    },
    handleSuccess(response, file, fileList) {
      //文件上传成功
      console.log(response, file, fileList);
      merge({
        name:file.name,
        fileHash:response[0].fileHash
      }).then(res=> {
      }).catch(() => {
      })
    },
    validatePgk:function (){
      return new Promise((resolve, reject) => {
        if(this.zookeeperselected==false && this.snowballselected == false ){
          reject('请选择要安装的组件！')
        }
        if(this.zookeeperselected){
          if(this.zookeeper.softlist.zookeeper==''||this.zookeeper.softlist.jdk==''){
            reject('请选择要安装的软件包！')
          }
        }
        if(this.snowballselected){
          if(this.snowball.softlist.common==''||this.snowball.softlist.server==''||this.snowball.softlist.client==''){
            reject('请选择要安装的软件包！')
          }
        }
        resolve(true)
      })
    },
    validateService:function() {
      return new Promise((resolve, reject) => {
        if(this.zookeeperselected){
          this.$refs['zookeeperForm'].validate((valid) => {
            if (valid) {
            } else {
              reject('表单输入有误！')
              return false;
            }
          });
          if(this.zookeeper.nodes.length==0){
            reject('不能为空！')
          }
          var zkorders = new Set(this.zookeeper.nodes.map(e=>{return e.order}));
          if(zkorders.size!=this.zookeeper.nodes.length){
            reject('序列重复！')
          }
          this.zookeeper.nodes.map(e=>{
            if(e.name.trim()==''){
              reject('zk节点名,不能为空！')
            }
          })
          var zkNames = new Set(this.zookeeper.nodes.map(e=>{return e.name}));
          if(zkNames.size!=this.zookeeper.nodes.length){
            reject('zk节点名重复！')
          }
          var zkServerNames = new Set(this.zookeeper.nodes.map(e=>{return e.ssh}));
          if(zkServerNames.size!=this.zookeeper.nodes.length){
            reject('zk节点服务器名重复！')
          }
        }
        if(this.snowballselected){
          this.$refs['snowballForm'].validate((valid) => {
            if (valid) {
            } else {
              reject('表单输入有误！')
              return false;
            }
          });
          if(this.snowball.nodes.length==0){
            reject('snowball 节点不能为空！')
          }
          this.snowball.nodes.map(e=>{
            if(e.name.trim()==''){
              reject('snowball节点名,不能为空！')
            }
          })
          var snowballNames = new Set(this.snowball.nodes.map(e=>{return e.name}));
          if(snowballNames.size!=this.snowball.nodes.length){
            reject('snowball节点名不能重复！')
          }
          var snowballServerNames = new Set(this.snowball.nodes.map(e=>{return e.ssh}));
          if(snowballServerNames.size!=this.snowball.nodes.length){
            reject('snowball节点服务器名重复！')
          }

        }
        resolve(true)
      })
    },
    validateHost:function() {
      return new Promise((resolve, reject) => {
        if(this.hosts.length==0){
          reject('不能为空！')
        }
        this.hosts.map(e=>{
          if(e.name.trim()==''){
            reject('服务器名,不能为空！')
          }
        })
        var serverNames = new Set(this.hosts.map(e=>{return e.name}));
        if(serverNames.size!=this.hosts.length){
          reject('服务器重名！')
        }
        var servers = new Set(this.hosts.map(e=>{return e.ip+":"+e.port}));
        if(servers.size!=this.hosts.length){
          reject('服务器地址重复！')
        }
        validateHost({hosts: this.hosts}).then(response => {
          const {data} = response
          let arr = data.map(e=>{return e.status})
          let index = arr.indexOf(false);
          if (index==-1){
            resolve(true)
          }
          reject('尝试连接服务器时出错！')
        }).catch(() => {
          reject('服务器配置错误！')
        })
      })
    },
    select(selections, row){
      selections.forEach(selection => {
        if(selection.service == 'zookeeper'){//#选中zookeeper组件
          this.zookeeperselected = true
        }
        if(selection.service == 'snowball') {
          this.snowballselected = true
        }
      });
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    rowSelectionSetting(row, index){
      var services = ["zookeeper", "snowball"];
      return services.includes(row.service)
    },
    handleChange(index,ip) {
      this.hosts[index].ip = ip
    },
    handleChangeSb(index,ip) {
      this.snowball.listen_host = ip
    },
    handleChangeSblisten(index,ip) {
      this.snowball.nodes[index].listen_host = ip
    },
    fileSelectionDlg() {
      let params = {
        'dialog_title': 'Select Folder',
        'dialog_type': 'storage_dialog_folder',
      };
      let show_dialog = pgAdmin.FileManager.show_dialog(params);
      //Alertify.fileSelectionDlg(params).resizeTo(pgAdmin.Browser.stdW.md,pgAdmin.Browser.stdH.lg);
      //pgAdmin.Browser.Events.on('pgadmin-storage:finish_btn:select_file', this.storage_dlg_hander, this);
      pgAdmin.Browser.Events.on('pgadmin-storage:finish_btn:storage_dialog_folder', this.storage_dlg_hander, this);
      //console.log(show_dialog)
    },
    forceClearError() {
    },
    storage_dlg_hander: function(value) {
      this.general.path=value.substring(0, value.lastIndexOf("/"))+'/'
    },
    setLoading: function(value) {
      this.loadingWizard = value
    },
    handleErrorMessage: function(errorMsg){
      this.errorMsg = errorMsg
    },
    handleValidation: function(isValid, tabIndex){
      console.log('Tab: '+tabIndex+ ' valid: '+isValid)
    },
    validateSource:function (){
      return new Promise((resolve, reject) => {
        list().then(res=> {
         // this.softlists = res.data
        }).catch(() => {

        })
        resolve(true)
      })
    },
    deleteRow(index, rows) {
      rows.splice(index, 1);
    },
    deleteRowZk(index, rows) {
      rows.splice(index, 1);
    },
    deleteRowSb(index, rows) {
      rows.splice(index, 1);
    },
    addzk() {
      this.zookeeper.nodes.push({
        name: 'zkX',
        order: '3',
        port1: '2181',
        port2: '2888',
        port3: '3888',
        ssh: 'nodeX'
      })
    },
    addsb() {
      this.snowball.nodes.push({
        name: 'node03',
        path:'/data/snowball/',
        tcp_port:'9000',
        http_port:'8123',
        interserver_http_port:'9090',
        listen_host:'0.0.0.0',
        timezone:'Asia/Shanghai',
        ssh: 'server3'
      })
    },
    add() {
      this.hosts.push({
        name: 'nodex',
        ip: '192.168.1.1',
        user: 'root',
        password: 'admin',
        port: '22',
        status: 1
      });
    },
    onComplete() {
      let c = setInterval(()=>{
        processer().then(_ => {
          const {data} = _
          this.percentage = data.percentage
        }).catch(() => {})
       /* if(this.num<100){
          this.num++
          this.percentage = this.num
        }else {
          this.num =0
        }*/
      }, 3000);

      setInstallConf({
        config: {
          zookeeperselected: this.zookeeperselected,
          snowballselected: this.snowballselected,
          general: this.general,
          hosts: this.hosts,
          zookeeper: this.zookeeper,
          snowball: this.snowball
        }
      }).then(response => {
        const {data} = response
        this.res = data
        this.installres = true
        this.percentage = 100
        clearInterval(c)
      }).catch(() => {
        clearInterval(c)
      })
    }
  }
}
</script>
<style>
.wizard-header{ background-color : #ffffff !important;}
.v-modal { z-index: 199 !important; }
.el-dialog__wrapper { z-index: 200 !important; }
.vue-form-wizard .wizard-header {
  padding: 15px;
  position: relative;
  border-radius: 3px 3px 0 0;
  text-align: center;
  background-color: #ffffff
}
.vue-form-wizard .wizard-title {
  font-size:20px;
  margin: 0;
  text-align: center;
}
span.error{
  color: #fa0202;
  font-size:14px;
  display:flex;
  justify-content:center;
}
</style>

