import Vue from 'vue'
import ElementUI from 'element-ui'
import FormWizard from "vue-form-wizard"

import "vue-form-wizard/dist/vue-form-wizard.min.css";
import 'element-ui/lib/theme-chalk/index.css'
import locale from 'element-ui/lib/locale/lang/zh-CN' // lang i18n
Vue.use(ElementUI, { locale })
Vue.use(FormWizard);

import App from './App.vue'



setTimeout(function() {
  var component = new Vue({
    render: function (createElement) {
      return createElement(App);
    }
  }).$mount('#install')
  // document.getElementById('install').appendChild(component.$el)
  // console.log("###document.getElementById('install').appendChild(component.$el)")
}, 2000);

