import Vue from 'vue'
import ElementUI from 'element-ui'
import FormWizard from "vue-form-wizard"

import "vue-form-wizard/dist/vue-form-wizard.min.css";
import 'element-ui/lib/theme-chalk/index.css'
import locale from 'element-ui/lib/locale/lang/zh-CN' // lang i18n

import pgAdmin from 'sources/pgadmin';

Vue.use(ElementUI, { locale })
Vue.use(FormWizard);


//export default Vue;
//import App from './App.vue'
import install from 'tools/install/static/js/install.vue'

setTimeout(function() {
  //console.log(pgAdmin.Browser.get_preference_for_id(45).value)
  var component = new Vue({
    render: function (createElement) {
      return createElement(install);
    }
  }).$mount('#install')
  // document.getElementById('install').appendChild(component.$el)
  // console.log("###document.getElementById('install').appendChild(component.$el)")
}, 3000);

