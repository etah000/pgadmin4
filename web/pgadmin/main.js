import Vue from 'vue'
import VueI18n from 'vue-i18n'
import ElementLocale from 'element-ui/lib/locale'
import enLocale from 'element-ui/lib/locale/lang/en'
import zhLocale from 'element-ui/lib/locale/lang/zh-CN'

import langZh from "./translations/zh.js"
import langEN from "./translations/en.js"
Vue.use(VueI18n)
const i18n = new VueI18n({
  locale: 'zh',
  messages: {
    'zh': {...langZh,...zhLocale},
    'en': {...langEN,...enLocale}
  }
})
ElementLocale.i18n((key, value) => i18n.t(key, value))
import ElementUI from 'element-ui'
import FormWizard from "vue-form-wizard"
import "vue-form-wizard/dist/vue-form-wizard.min.css";
import 'element-ui/lib/theme-chalk/index.css'
import locale from 'element-ui/lib/locale/lang/zh-CN' // lang i18n

import pgAdmin from 'sources/pgadmin';
import axios from 'axios'
Vue.use(ElementUI, { locale })
Vue.use(FormWizard);


//export default Vue;
//import App from './App.vue'
import install from 'tools/install/static/js/install.vue'

setTimeout(function() {
  //console.log(pgAdmin.Browser.get_preference_for_id(45).value) 主题 standard dark
  //console.log(pgAdmin.Browser.get_preference_for_id(44).value) 语言 en zh
  axios.get('/preferences/get_all')
    .then(function (response) {
      i18n.locale = response.data.find(e=>e.name=="user_language").value
        new Vue({
          i18n,
          render: function (createElement) {
            return createElement(install);
          }
        }).$mount('#install')
      })
    .catch(function (error) {
      console.log(error);
    });
  // document.getElementById('install').appendChild(component.$el)
  // console.log("###document.getElementById('install').appendChild(component.$el)")
}, 3000);


import wrapper from '@vue/web-component-wrapper'
import MyComponent from "./App.vue";

const CustomElement = wrapper(Vue, MyComponent)
window.customElements.define('my-component', CustomElement)
