//import Vue from 'top/main'
//import install from 'tools/install/static/js/install.vue'
define([
  'sources/gettext', 'sources/url_for', 'jquery', 'underscore', 'pgadmin.alertifyjs',
  'sources/pgadmin', 'pgadmin.browser'
], function(
  gettext, url_for, $, _, Alertify, pgAdmin, pgBrowser
) {
  pgAdmin = pgAdmin || window.pgAdmin || {};
  var pgTools = pgAdmin.Tools = pgAdmin.Tools || {};
  // Return back, this has been called more than once
  if (pgAdmin.Tools.install)
    return pgAdmin.Tools.install;
  pgTools.install = {
    init: function() {
      // We do not want to initialize the module multiple times.
      if (this.initialized)
        return;
      this.initialized = true;
      // Initialize the context menu to display the import options when user open the context menu for table
      /*pgBrowser.add_menus([{
        name: 'install',
        module: this,
        applies: ['tools'],
        callback: 'callback_install',
        category: 'tools',
        priority: 10,
        label: gettext('Install'),
        icon: 'fa fa-shopping-cart',
      }]);*/
    },
    initVue: function() {
      if (this.vueinited)
        return;
      this.vueinited = true;
     // new Vue({render: h=> h(install)}).$mount('#install')
    },
    callback_install: function(args, item) {
    }
  };

  return pgAdmin.Tools.install;
});
