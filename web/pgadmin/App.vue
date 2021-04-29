<template>
  <a id="install" href="#" data-toggle="pg-menu" role="menuitem" class="dropdown-item">
    <span data-test="menu-item-text"  @click="dialogFormVisible = true">  Install...</span>
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
          <tab-content title="一般设置" icon="el-icon-coin" :before-change="validatePgk" >
            <el-form :model="general"  ref="generalForm" :rules="rulesGeneral"  size="medium">
              <el-form-item label="软件路径" :label-width="formLabelWidth" prop="path">
                <el-input v-model="general.path" autocomplete="off"></el-input>
                <el-button @click="fileSelectionDlg" size="medium" icon="el-icon-circle-plus-outline" type="primary" round>选取
                </el-button>
              </el-form-item>
            </el-form>
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
                  <el-input  size="small" v-model="scope.row.name"></el-input>
                </template>
              </el-table-column>
              <el-table-column
                  prop="ip"
                  label="ip地址：ssh端口"
                  width = "300"
                  >
                <template slot-scope="scope">
                  <vue-ip  size="small" :ip="scope.row.ip" :port="scope.row.port"></vue-ip>
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
          <tab-content title="zookeeper 设置" icon="el-icon-setting" :before-change="validateZk">
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
                    <el-button @click="addzk" size="medium" icon="el-icon-circle-plus-outline" type="primary" round>添加Zk节点</el-button>
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
                      <el-table-column prop="ssh" label="服务器名">
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
          </tab-content>
          <tab-content title="snowball 设置" icon="el-icon-orange" :before-change="validateSnowball">
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
                    <vue-ip  size="small" :ip="snowball.listen_host"  autocomplete="off">></vue-ip>
                  </el-form-item>
                </el-col>
              </el-row>
              <el-row>
                <el-col :span="24">
                  <el-form-item label="interserver_http_port" label-width="160px" prop="interserver_http_port">
                    <el-input v-model="snowball.interserver_http_port" autocomplete="off"></el-input>
                  </el-form-item>
                </el-col>
              </el-row>
              <el-row>
                <el-col :span="24">
                  <el-form-item label="nodes" :label-width="formLabelWidth" prop="nodes">
                    <el-checkbox-group v-model="snowball.nodes">
                      <el-checkbox v-for="host in hosts" :label="host.name" :key="host.name">{{host.name}}</el-checkbox>
                    </el-checkbox-group>
                  </el-form-item>
                </el-col>
              </el-row>
            </el-form>
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
import {getInstallConf, setInstallConf,validateConf,validateHost} from './static/js/api/install.js'
import VueIp from 'Vue-Ip';
import VueIpInput from 'vue-ip-input'

export default {
  components: {
    VueIp,
    VueIpInput
  },
  name: 'install',
  data: function () {
    return {
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
        path:'/soft/'
      },
      hosts: [
        {name: 'node1', ip: '192.168.2.184', user: 'root', password: 'admin', port: '1023', status: 1},
        {name: 'node2', ip: '192.168.2.184', user: 'root', password: 'admin', port: '1024', status: 1},
        {name: 'node3', ip: '192.168.2.184', user: 'root', password: 'admin', port: '1025', status: 1}],
      zookeeper: {
        tickTime: '2000',
        initLimit: '10',
        syncLimit: '5',
        dataDir: '/data/zookeeper',
        clientPort: '2181',
        nodes: [
          {name: 'zk001', order: '1', port1: '2181', port2: '2888', port3: '3888', ssh: 'node1'},
          {name: 'zk002', order: '2', port1: '2181', port2: '2888', port3: '3889', ssh: 'node2'},
          {name: 'zk003', order: '3', port1: '2181', port2: '2888', port3: '3890', ssh: 'node3'}
        ]
      },
      snowball: {
        datadir: '/data',
        tcp_port: '9000',
        http_port: '8123',
        interserver_http_port: '9090',
        listen_host: '0.0.0.0',
        nodes: ['node1','node2','node3']
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
    fileSelectionDlg() {
      let params = {
        'dialog_title': 'Select file',
        'dialog_type': 'select_file',
      };

      let show_dialog = pgAdmin.FileManager.show_dialog(params);
      //Alertify.fileSelectionDlg(params).resizeTo(pgAdmin.Browser.stdW.md,pgAdmin.Browser.stdH.lg);
      pgAdmin.Browser.Events.on('pgadmin-storage:finish_btn:select_file', this.storage_dlg_hander, this);
      //console.log(show_dialog)
    },
    forceClearError() {
    },
    storage_dlg_hander: function(value) {
      this.general.path=value
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
    validatePgk:function (){
      return new Promise((resolve, reject) => {
        resolve(true)
      })
    },
    validateSnowball: function () {
      return new Promise((resolve, reject) => {
        this.$refs['snowballForm'].validate((valid) => {
          if (valid) {
          } else {
            reject('表单输入有误！')
            return false;
          }
        });
        var snowballnodes = new Set(this.snowball.nodes);
        if(snowballnodes.size!=this.snowball.nodes.length){
          reject("snowball节点服务器名重复")
        }
        resolve(true)
      })
    },
    validateZk: function () {
      return new Promise((resolve, reject) => {
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
        var zkNames = new Set(this.zookeeper.nodes.map(e=>{return e.name}));
        if(zkNames.size!=this.zookeeper.nodes.length){
          reject('zk节点名重复！')
        }
        var zkServerNames = new Set(this.zookeeper.nodes.map(e=>{return e.ssh}));
        if(zkServerNames.size!=this.zookeeper.nodes.length){
          reject('zk节点服务器名重复！')
        }
        resolve(true)
      })
    },
    validateHost:function() {
      return new Promise((resolve, reject) => {
        if(this.hosts.length==0){
          reject('不能为空！')
        }
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
    deleteRow(index, rows) {
      rows.splice(index, 1);
    },
    deleteRowZk(index, rows) {
      rows.splice(index, 1);
    },
    addzk() {
      this.zookeeper.nodes.push({
        name: 'zkX',
        order: '3',
        port1: '2181',
        port2: '2888',
        port3: '3890',
        ssh: 'nodeX'
      })
    },
    add() {
      this.hosts.push({
        name: 'nodex',
        ip: '192.168.1.1',
        user: 'root',
        password: '******',
        port: '22',
        status: 1
      });
    },
    onComplete() {
      let c = setInterval(()=>{
        if(this.num<100){
          this.num++
          this.percentage = this.num
        }else {
          this.num =0
        }
      }, 5000);
      setInstallConf({
        config: {
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
  font-size:20px;
  display:flex;
  justify-content:center;
}
</style>

