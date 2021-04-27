define([
  'sources/gettext', 'sources/url_for', 'jquery', 'underscore', 'pgadmin.alertifyjs',
  'sources/pgadmin', 'pgadmin.browser', 'backbone', 'backgrid', 'backform',
  'sources/utils',
  'sources/nodes/supported_database_node',
  'pgadmin.backform', 'pgadmin.backgrid', 'pgadmin.browser.node.ui',
], function(
  gettext, url_for, $, _, Alertify, pgAdmin, pgBrowser, Backbone, Backgrid,
  Backform, commonUtils, supportedNodes
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
      pgBrowser.add_menus([{
        name: 'install',
        module: this,
        applies: ['tools'],
        category: 'tools',
        priority: 10,
        label: gettext('Install...'),
        icon: 'fa fa-shopping-cart',
      }]);
    },
    createButtons: function(buttons, location, extraClasses) {
      // Arguments must be non-zero length array of type
      // object, which contains following attributes:
      // label, type, extraClasses, register
      if (buttons && _.isArray(buttons) && buttons.length > 0) {
        // All buttons will be created within a single
        // div area.
        var btnGroup =
            $('<div class="pg-prop-btn-group"></div>'),
          // Template used for creating a button
          tmpl = _.template([
            '<button tabindex="0" type="<%= type %>" ',
            'class="btn <%=extraClasses.join(\' \')%>"',
            '<% if (disabled) { %> disabled="disabled"<% } %> title="<%-tooltip%>"',
            '<% if (label != "") {} else { %> aria-label="<%-tooltip%>"<% } %> >',
            '<span class="<%= icon %>"></span><% if (label != "") { %>&nbsp;<%-label%><% } %></button>',
          ].join(' '));
        if (location == 'header') {
          btnGroup.appendTo($('.ajs-footer'));
        } else {
          btnGroup.appendTo($('.ajs-footer'));
        }
        if (extraClasses) {
          btnGroup.addClass(extraClasses);
        }
        _.each(buttons, function(btn) {
          // Create the actual button, and append to
          // the group div

          // icon may not present for this button
          if(btn.visible){
            return true;
          }
          if (!btn.icon) {
            btn.icon = '';
          }
          var b = $(tmpl(btn));
          btnGroup.append(b);
          // Register is a callback to set callback
          // for certain operation for this button.
          btn.register(b);
        });
        return btnGroup;
      }
      return null;
    },
    callback_install: function(args, item) {
      var that = this
      if(!Alertify.installAlert){
        //define a new dialog
        Alertify.dialog('installAlert',function(){
          return{
            main:function(title){
              this.set('title', title);
            },
            setup:function(){
              return {
                buttons:[
                  {text: "Cancel", attrs:{type:'cancel'},className:"btn btn-secondary mx-1"},
                  {text: "Reset", attrs:{type:'reset'},className:"btn btn-secondary mx-1"},
                  {text: "Save", attrs:{type:'save'},className:"btn btn-secondary mx-1"}],
                focus: { element:0 }
              };
            },
            prepare:function(){
              that.createButtons([{
                  label: gettext('Reset'),
                  type: 'reset',
                  tooltip: gettext('Reset the fields on this dialog.'),
                  extraClasses: ['btn-secondary', 'mx-1'],
                  icon: 'fa fa-recycle pg-alertify-button',
                  disabled: true,
                  register: function(btn) {},
                }], 'footer', 'pg-prop-btn-group-below');
            }
          }});
      }
      Alertify.installAlert("install").resizeTo(pgBrowser.stdW.lg,pgBrowser.stdH.lg);
      var newModel =new Backbone.Model.extend({});
      new Backform.Dialog({
        /*el: $container,*/
        model: newModel,
       /* schema: fields,*/
      }).render();
    },
  };

  return pgAdmin.Tools.install;
});
