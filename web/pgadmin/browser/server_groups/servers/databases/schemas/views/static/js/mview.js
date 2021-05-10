/////////////////////////////////////////////////////////////
//
// pgAdmin 4 - PostgreSQL Tools
//
// Copyright (C) 2013 - 2020, The pgAdmin Development Team
// This software is released under the PostgreSQL Licence
//
//////////////////////////////////////////////////////////////

define('pgadmin.node.mview', [
  'sources/gettext', 'sources/url_for', 'jquery', 'underscore',
  'sources/pgadmin', 'pgadmin.alertifyjs', 'pgadmin.browser',
  'pgadmin.backform', 'pgadmin.node.schema.dir/child',
  'pgadmin.node.schema.dir/schema_child_tree_node', 'pgadmin.browser.server.privilege',
  'pgadmin.browser.collection', 'pgadmin.node.column',
  'pgadmin.node.constraints', 'pgadmin.browser.table.partition.utils',
], function(
  gettext, url_for, $, _, pgAdmin, Alertify, pgBrowser, Backform,
  schemaChild, schemaChildTreeNode
) {

  /**
    Create and add a view collection into nodes
    @param {variable} label - Label for Node
    @param {variable} type - Type of Node
    @param {variable} columns - List of columns to
      display under under properties.
   */
  if (!pgBrowser.Nodes['coll-mview']) {
    pgBrowser.Nodes['coll-mview'] =
      pgBrowser.Collection.extend({
        node: 'mview',
        label: gettext('Materialized Views'),
        type: 'coll-mview',
        columns: ['name', 'engine', 'database'],
        canDrop: schemaChildTreeNode.isTreeItemOfChildOfSchema,
        canDropCascade: schemaChildTreeNode.isTreeItemOfChildOfSchema,
        hasStatistics: false,
      });
  }

  /**
    Create and Add a View Node into nodes
    @param {variable} parent_type - The list of nodes
    under which this node to display
    @param {variable} type - Type of Node
    @param {variable} hasSQL - To show SQL tab
    @param {variable} canDrop - Adds drop view option
    in the context menu
    @param {variable} canDropCascade - Adds drop Cascade
    view option in the context menu
   */
  if (!pgBrowser.Nodes['mview']) {
    pgBrowser.Nodes['mview'] = schemaChild.SchemaChildNode.extend({
      parent_type: 'database',
      type: 'mview',
      sqlAlterHelp: 'sql-altermaterializedview.html',
      sqlCreateHelp: 'sql-creatematerializedview.html',
      dialogHelp: url_for('help.static', {'filename': 'materialized_view_dialog.html'}),
      label: gettext('Materialized View'),
      hasSQL: true,
      populate:false,
      canEdit: false,
      canDrop: true,
      canDropCascade: false,
      hasDepends: true,
      hasScriptTypes: ['create', 'select'],
      collection_type: 'coll-mview',
      width: pgBrowser.stdW.md + 'px',
      Init: function() {

        // Avoid mulitple registration of menus
        if (this.initialized)
          return;

        this.initialized = true;

        /**
          Add "create view" menu option into context and object menu
          for the following nodes:
          coll-mview, view and schema.
          @property {data} - Allow create view option on schema node or
          system view nodes.
         */
        // pgAdmin.Browser.add_menu_category(
        //   'refresh_mview', gettext('Refresh View'), 18, '');
        pgBrowser.add_menus([
          {
          name: 'create_mview_on_coll', node: 'coll-mview', module: this,
          applies: ['object', 'context'], callback: 'show_obj_properties',
          category: 'create', priority: 1, icon: 'wcTabIcon icon-mview',
          data: {action: 'create', check: true}, enable: 'canCreate',
          label: gettext('Materialized View...'),
        },
        {
          name: 'create_mview_on_database', node: 'database', module: this,
          applies: ['object', 'context'], callback: 'show_obj_properties',
          category: 'create', priority: 9, icon: 'wcTabIcon icon-mview',
          data: {action: 'create', check: true}, enable: false,
          label: gettext('Materialized View...'),
        },
        {
          name: 'create_mview', node: 'coll-mview', module: this,
          applies: ['object', 'context'], callback: 'show_obj_properties',
          category: 'create', priority: 1, icon: 'wcTabIcon icon-mview',
          data: {action: 'create', check: true}, enable: false,
          label: gettext('Materialized View...'),
        },
      // {
      //   name: 'create_mview', node: 'schema', module: this,
      //   applies: ['object', 'context'], callback: 'show_obj_properties',
      //   category: 'create', priority: 18, icon: 'wcTabIcon icon-mview',
      //   data: {action: 'create', check: false}, enable: 'canCreate',
      //   label: gettext('Materialized View...'),
      // },
      //  {
      //     name: 'refresh_mview_data', node: 'mview', module: this,
      //     priority: 1, callback: 'refresh_mview', category: 'refresh_mview',
      //     applies: ['object', 'context'], label: gettext('With data'),
      //     data: {concurrent: false, with_data: true}, icon: 'fa fa-recycle',
      //   },{
      //     name: 'refresh_mview_nodata', node: 'mview',
      //     callback: 'refresh_mview', priority: 2, module: this,
      //     category: 'refresh_mview', applies: ['object', 'context'],
      //     label: gettext('With no data'), data: {
      //       concurrent: false, with_data: false,
      //     }, icon: 'fa fa-refresh',
      //   },{
      //     name: 'refresh_mview_concurrent', node: 'mview', module: this,
      //     category: 'refresh_mview', enable: 'is_version_supported',
      //     data: {concurrent: true, with_data: true}, priority: 3,
      //     applies: ['object', 'context'], callback: 'refresh_mview',
      //     label: gettext('With data (concurrently)'), icon: 'fa fa-recycle',
      //   },{
      //     name: 'refresh_mview_concurrent_nodata', node: 'mview', module: this,
      //     category: 'refresh_mview', enable: 'is_version_supported',
      //     data: {concurrent: true, with_data: false}, priority: 4,
      //     applies: ['object', 'context'], callback: 'refresh_mview',
      //     label: gettext('With no data (concurrently)'),
      //     icon: 'fa fa-refresh',
      //   }
        ]);
      },

      /**
        Define model for the view node and specify the
        properties of the model in schema.
       */
      model: pgBrowser.Node.Model.extend({
        idAttribute: 'oid',
        initialize: function(attrs, args) {
          if (_.size(attrs) === 0) {
            // Set Selected Schema and Current User
            // var schemaLabel = args.node_info.schema._label || 'public',
            //   userInfo = pgBrowser.serverInfo[args.node_info.server._id].user;
            // this.set({
            //   'schema': schemaLabel, 'owner': userInfo.name,
            // }, {silent: true});
          }
          pgBrowser.Node.Model.prototype.initialize.apply(this, arguments);
        },
        defaults: {
          spcname: undefined,
          // toast_autovacuum_enabled: 'x',
          // autovacuum_enabled: 'x',
          populate:false,
          warn_text: undefined,
        },
        schema: [
          {
          id: 'name', label: gettext('Name'), cell: 'string',
          type: 'text', disabled: 'inSchema',
        },
        {
          id: 'database', label: gettext('Database'), cell: 'string',
          type: 'text', disabled: 'inSchema',
        },
        {
          id: 'cluster', label: gettext('On Cluster'), type: 'text', node: 'cluster',
          mode: ['edit','create'], select2: {allowClear: true},
          control: 'node-list-by-name',
        },
        {
          id: 'engine', label: gettext('Engine'),
          control: 'select2',
          type: 'text', mode: ['properties','create'],
          options: [
            {label: gettext('请选择'), value: ''},
            {label: gettext('MergeTree'), value: 'MergeTree'},
            // {label: gettext('Distributed'), value: 'Distributed'}
          ],
          control: Backform.SelectControl.extend({
            onChange: function() {
              Backform.SelectControl.prototype.onChange.apply(this, arguments);
              let engine=this.model.get('engine');
              if(engine!=''){
                document.querySelector('.to_database').classList.add("d-none"); 
                document.querySelector('.to_table').classList.add("d-none");
                document.querySelector('.engine_params').classList.remove("d-none");
              }else{
                document.querySelector('.to_database').classList.remove("d-none");
                document.querySelector('.to_table').classList.remove("d-none");
                document.querySelector('.engine_params').classList.add("d-none");
              }
              console.log(engine);
            },
          }),
          select2: { allowClear: false, width: '100%' },
        },
        // {
        //   id: 'engine_params', label: gettext('Engine Params'), cell: 'string',
        //   type: 'text', mode: ['properties','create', 'edit'], 
        // },
        {
          id: 'to_database', label: gettext('To Database'), cell: 'string',
          type: 'text', disabled: 'inSchema',
        },
        {
          id: 'to_table', label: gettext('To Table'), cell: 'string',
          type: 'text', disabled: 'inSchema',
        },
          // {
        //   id: 'shifted', label: gettext('shifted'), type: 'options', mode: ['create'],
        //   options: [
        //     {label: gettext('true'), value: 'true'},
        //     {label: gettext('false'), value: 'false'},
        //   ],select2: { allowClear: false, width: '100%' },
        // },
           {
          id: 'populate', label: gettext('Populate'), type: 'switch',
          mode: ['create'],'options': {
            'onText':  gettext('True'), 'offText':  gettext('False'), 'size': 'mini',
          },
        },
        // {
        //   id: 'cluster', label: gettext('On Cluster'), type: 'text', node: 'cluster',
        //   mode: ['edit','create'], select2: {allowClear: true},
        //   control: 'node-list-by-name',
        // },
        {
          id: 'order_keys', label: gettext('Order Keys'), cell: 'string',
          type: 'text', mode: ['properties','create', 'edit'],
        },
        {
          id: 'partition_keys', label: gettext('Partition Keys'), cell: 'string',
          type: 'text', mode: ['properties','create', 'edit'],
        },
        //{
        //   id: 'system_view', label: gettext('System materialized view?'), cell: 'string',
        //   type: 'switch', mode: ['properties'],
        // }, pgBrowser.SecurityGroupSchema, {
        //   id: 'acl', label: gettext('Privileges'),
        //   mode: ['properties'], type: 'text', group: gettext('Security'),
        // },
        {
          id: 'definition', label: gettext('Definition'), cell: 'string',
          type: 'text', mode: ['create', 'edit'], group: gettext('Definition'),
          tabPanelCodeClass: 'sql-code-control',
          control: Backform.SqlCodeControl.extend({
            onChange: function() {
              Backform.SqlCodeControl.prototype.onChange.apply(this, arguments);
              if(this.model && this.model.changed) {
                if(this.model.origSessAttrs && (this.model.changed.definition != this.model.origSessAttrs.definition)) {
                  this.model.warn_text = gettext(
                    'Updating the definition will drop and re-create the materialized view. It may result in loss of information about its dependent objects.'
                  ) + '<br><br><b>' + gettext('Do you want to continue?') +
                    '</b>';
                }
                else {
                  this.model.warn_text = undefined;
                }
              }
              else {
                this.model.warn_text = undefined;
              }
            },
          }),
        },
       {
          // Here - we will create tab control for storage parameters
          // (auto vacuum).
          type: 'nested', control: 'tab', group: gettext('Settings'),
          mode: ['edit', 'create'], deps: ['is_partitioned'],
          schema: [
            {
              id: 'settings', label: '',
              model: pgBrowser.Nodes['unique_constraint'].model,
              subnode: pgBrowser.Nodes['unique_constraint'].model,
              editable: false, type: 'collection',
              group: gettext('Settings'), mode: ['edit', 'create'],
              canEdit: false, canDelete: true, deps:['is_partitioned'],
              control: 'unique-col-collection',
              canAdd: true,
              columns : ['label','value'],
            },
        ],
        },
        // {
        //   id: 'with_data', label: gettext('With data?'),
        //   group: gettext('Storage'), mode: ['edit', 'create'],
        //   type: 'switch',
        // },{
        //   id: 'fillfactor', label: gettext('Fill factor'),
        //   group: gettext('Storage'), mode: ['edit', 'create'],
        //   type: 'int', min: 10, max: 100,
        // },
        // {
        //   type: 'nested', control: 'tab', id: 'materialization',
        //   label: gettext('Parameter'), mode: ['edit', 'create'],
        //   group: gettext('Parameter'),
        //   schema: Backform.VacuumSettingsSchema,
        // }
        // ,{
        //   // Add Privilege Control
        //   id: 'datacl', label: gettext('Privileges'), type: 'collection',
        //   model: pgBrowser.Node.PrivilegeRoleModel.extend({
        //     privileges: ['a', 'r', 'w', 'd', 'D', 'x', 't'],
        //   }), uniqueCol : ['grantee'], editable: false,
        //   group: 'security', canAdd: true, canDelete: true,
        //   mode: ['edit', 'create'], control: 'unique-col-collection',
        // },{
        // // Add Security Labels Control
        //   id: 'seclabels', label: gettext('Security labels'),
        //   model: pgBrowser.SecLabelModel, editable: false, type: 'collection',
        //   canEdit: false, group: 'security', canDelete: true,
        //   mode: ['edit', 'create'], canAdd: true,
        //   control: 'unique-col-collection', uniqueCol : ['provider'],
        // }
      ],
        sessChanged: function() {
          /* If only custom autovacuum option is enabled the check if the options table is also changed. */
          if(_.size(this.sessAttrs) == 2 && this.sessAttrs['autovacuum_custom'] && this.sessAttrs['toast_autovacuum']) {
            return this.get('vacuum_table').sessChanged() || this.get('vacuum_toast').sessChanged();
          }
          if(_.size(this.sessAttrs) == 1 && (this.sessAttrs['autovacuum_custom'] || this.sessAttrs['toast_autovacuum'])) {
            return this.get('vacuum_table').sessChanged() || this.get('vacuum_toast').sessChanged();
          }
          return pgBrowser.DataModel.prototype.sessChanged.apply(this);
        },
        validate: function(keys) {

          // Triggers specific error messages for fields
          var err = {},
            errmsg,
            field_name = this.get('name'),
            field_def = this.get('definition');

          if(_.indexOf(keys, 'autovacuum_custom'))
            if (_.indexOf(keys, 'autovacuum_enabled') != -1 ||
              _.indexOf(keys, 'toast_autovacuum_enabled') != -1 )
              return null;

          if (_.isUndefined(field_name) || _.isNull(field_name) ||
            String(field_name).replace(/^\s+|\s+$/g, '') == '') {
            err['name'] = gettext('Please specify name.');
            errmsg = errmsg || err['name'];
            this.errorModel.set('name', errmsg);
            return errmsg;
          }else{
            this.errorModel.unset('name');
          }
          if (_.isUndefined(field_def) || _.isNull(field_def) ||
            String(field_def).replace(/^\s+|\s+$/g, '') == '') {
            err['definition'] = gettext('Please enter view definition.');
            errmsg = errmsg || err['definition'];
            this.errorModel.set('definition', errmsg);
            return errmsg;
          }else{
            this.errorModel.unset('definition');
          }
          return null;
        },
        // We will disable everything if we are under catalog node
        inSchema: function() {
          if(this.node_info && 'catalog' in this.node_info)
          {
            return true;
          }
          return false;
        },

      }),

      refresh_mview: function(args) {
        var input = args || {},
          obj = this,
          t = pgBrowser.tree,
          i = input.item || t.selected(),
          d = i && i.length == 1 ? t.itemData(i) : undefined,
          server_data = null;

        if (!d)
          return false;

        let j = i;
        while (j) {
          var node_data = pgBrowser.tree.itemData(j);
          if (node_data._type == 'server') {
            server_data = node_data;
            break;
          }

          if (pgBrowser.tree.hasParent(j)) {
            j = $(pgBrowser.tree.parent(j));
          } else {
            Alertify.alert(gettext('Please select server or child node from tree.'));
            break;
          }
        }

        if (!server_data) {
          return;
        }

        var module = 'paths',
          preference_name = 'pg_bin_dir',
          msg = gettext('Please configure the PostgreSQL Binary Path in the Preferences dialog.');

        if ((server_data.type && server_data.type == 'ppas') ||
          server_data.server_type == 'ppas') {
          preference_name = 'ppas_bin_dir';
          msg = gettext('Please configure the EDB Advanced Server Binary Path in the Preferences dialog.');
        }

        var preference = pgBrowser.get_preference(module, preference_name);

        if (preference) {
          if (!preference.value) {
            Alertify.alert(gettext('Configuration required'), msg);
            return;
          }
        } else {
          Alertify.alert(gettext('Failed to load preference %s of module %s', preference_name, module));
          return;
        }

        $.ajax({
          url: obj.generate_url(i, 'check_utility_exists' , d, true),
          type: 'GET',
          dataType: 'json',
        }).done(function(res) {
          if (!res.success) {
            Alertify.alert(
              gettext('Utility not found'),
              res.errormsg
            );
            return;
          }
          // Make ajax call to refresh mview data
          $.ajax({
            url: obj.generate_url(i, 'refresh_data' , d, true),
            type: 'PUT',
            data: {'concurrent': args.concurrent, 'with_data': args.with_data},
            dataType: 'json',
          })
            .done(function(res) {
              if (res.data && res.data.status) {
              //Do nothing as we are creating the job and exiting from the main dialog
                Alertify.success(res.data.info);
                pgBrowser.Events.trigger('pgadmin-bgprocess:created', obj);
              } else {
                Alertify.alert(
                  gettext('Failed to create materialized view refresh job.'),
                  res.errormsg
                );
              }
            })
            .fail(function(xhr, status, error) {
              Alertify.pgRespErrorNotify(
                xhr, error, gettext('Failed to create materialized view refresh job.')
              );
            });
        }).fail(function() {
          Alertify.alert(
            gettext('Utility not found'),
            gettext('Failed to fetch Utility information')
          );
          return;
        });
      },

      is_version_supported: function(data, item) {
        var t = pgAdmin.Browser.tree,
          i = item || t.selected(),
          d = data || (i && i.length == 1 ? t.itemData(i): undefined),
          node = this || (d && pgAdmin.Browser.Nodes[d._type]),
          info = node.getTreeNodeHierarchy.apply(node, [i]),
          version = info.server.version;

        // disable refresh concurrently if server version is 9.3
        return (version >= 90400);
      },
    });
  }

  return pgBrowser.Nodes['mview'];
});
