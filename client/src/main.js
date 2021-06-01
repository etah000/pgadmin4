import Vue from 'vue'
import VueI18n from 'vue-i18n'
import ElementLocale from 'element-ui/lib/locale'
import enLocale from 'element-ui/lib/locale/lang/en'
import zhLocale from 'element-ui/lib/locale/lang/zh-CN'

import langZh from "./i18n/zh.js"
import langEN from "./i18n/en.js"
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



Vue.use(ElementUI, { locale })
Vue.use(FormWizard);


//export default Vue;
//import App from './App.vue'
import install from './install.vue'

i18n.locale = 'zh'
new Vue({
  i18n,
  render: function (createElement) {
    return createElement(install);
  }
}).$mount('#app')


