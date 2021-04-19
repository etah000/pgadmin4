/////////////////////////////////////////////////////////////
//
// pgAdmin 4 - PostgreSQL Tools
//
// Copyright (C) 2013 - 2020, The pgAdmin Development Team
// This software is released under the PostgreSQL Licence
//
//////////////////////////////////////////////////////////////

define('pgadmin.node.view', [
  'sources/gettext', 'sources/url_for', 'jquery', 'underscore',
  'sources/pgadmin', 'pgadmin.browser', 'pgadmin.backform',
  'pgadmin.node.schema.dir/child', 'pgadmin.node.schema.dir/schema_child_tree_node',
  'pgadmin.browser.server.privilege', 'pgadmin.node.rule',
], function(
  gettext, url_for, $, _, pgAdmin, pgBrowser, Backform, schemaChild, schemaChildTreeNode
) {


  /**
    Create and add a view collection into nodes
    @param {variable} label - Label for Node
    @param {variable} type - Type of Node
    @param {variable} columns - List of columns to
      display under under properties.
   */
  if (!pgBrowser.Nodes['coll-view']) {
    pgBrowser.Nodes['coll-view'] =
      pgBrowser.Collection.extend({
        node: 'view',
        label: gettext('Views'),
        type: 'coll-view',
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
   */
  if (!pgBrowser.Nodes['view']) {
    pgBrowser.Nodes['view'] = schemaChild.SchemaChildNode.extend({
      parent_type: 'database',
      type: 'view',
      sqlAlterHelp: 'sql-alterview.html',
      sqlCreateHelp: 'sql-createview.html',
      dialogHelp: url_for('help.static', {'filename': 'view_dialog.html'}),
      label: gettext('View'),
      hasSQL:  true,
      canEdit: true,
      canDrop: true,
      canDropCascade: false,
      hasDepends: true,
      hasScriptTypes: ['create', 'select'],
      collection_type: 'coll-view',
      Init: function() {

        // Avoid mulitple registration of menus
        if (this.initialized)
          return;

        this.initialized = true;

        /**
          Add "create view" menu option into context and object menu
          for the following nodes:
          coll-view, view and schema.
          @property {data} - Allow create view option on schema node or
          system view nodes.
          */
        pgBrowser.add_menus([
          {
          name: 'create_view_on_coll', node: 'coll-view', module: this,
          applies: ['object', 'context'], callback: 'show_obj_properties',
          category: 'create', priority: 1, label: gettext('View...'),
          icon: 'wcTabIcon icon-view', data: {action: 'create', check: true},
          enable: 'canCreate',
        },
        {
          name: 'create_view', node: 'view', module: this,
          applies: ['object', 'context'], callback: 'show_obj_properties',
          category: 'create', priority: 1, label: gettext('View...'),
          icon: 'wcTabIcon icon-view', data: {action: 'create', check: true},
          enable: 'canCreate',
        },
        {
          name: 'create_view', node: 'coll-view', module: this,
          applies: ['object', 'context'], callback: 'show_obj_properties',
          category: 'create', priority: 1, label: gettext('View...'),
          icon: 'wcTabIcon icon-view', data: {action: 'create', check: true},
          enable: false,
        },
        { 
          name: 'create_view_on_database', node: 'database', module: this,
          applies: ['object', 'context'], callback: 'show_obj_properties',
          category: 'create', priority: 8, label: gettext('View...'),
          icon: 'wcTabIcon icon-view', data: {action: 'create', check: false},
          enable: false,
        },
        // {
        //   name: 'create_view', node: 'schema', module: this,
        //   applies: ['object', 'context'], callback: 'show_obj_properties',
        //   category: 'create', priority: 17, label: gettext('View...'),
        //   icon: 'wcTabIcon icon-view', data: {action: 'create', check: false},
        //   enable: 'canCreate',
        // },
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
            // Set Selected Schema and, Current User
            // var schemaLabel = args.node_info.schema._label || 'public',
            //   userInfo = pgBrowser.serverInfo[args.node_info.server._id].user;
            // this.set({
            //   'schema': schemaLabel, 'owner': userInfo.name,
            // }, {silent: true});
          }
          pgBrowser.Node.Model.prototype.initialize.apply(this, arguments);
        },
        schema: [{
          id: 'name', label: gettext('Name'), cell: 'string',
          mode: ['create','properties'],
          type: 'text', disabled: 'notInSchema',
        },{
          id: 'engine', label: gettext('Engine'), cell: 'string',
          type: 'text', mode: ['properties'],
        },
        {
          id: 'on_cluster', label: gettext('On Cluster'), type: 'text', node: 'cluster',
          mode: ['edit','create','properties'], select2: {allowClear: true},
          control: 'node-list-by-name',
        },
        {
          id: 'database', label: gettext('Database'), cell: 'string',
          type: 'text', mode: ['create', 'edit','properties'],
        },{
          id: 'schema', label: gettext('Schema'), cell: 'string', first_empty: false,
          control: 'node-list-by-name', type: 'text', cache_level: 'database',
          node: 'schema', disabled: 'notInSchema', mode: [],
          select2: { allowClear: false }, cache_node: 'database',
        // },{
        //   id: 'system_view', label: gettext('System view?'), cell: 'string',
        //   type: 'switch', mode: ['properties'],
        // },{
        //   id: 'acl', label: gettext('Privileges'),
        //   mode: ['properties'], type: 'text', group: gettext('Security'),
        },
        {
          id: 'definition', label: gettext('Definition'), cell: 'string',
          type: 'text', mode: ['create', 'edit'], group: gettext('Definition'),
          tabPanelCodeClass: 'sql-code-control',
          disabled: 'notInSchema',
          control: Backform.SqlCodeControl.extend({
            onChange: function() {
              Backform.SqlCodeControl.prototype.onChange.apply(this, arguments);

              if (!this.model || !(
                this.model.changed &&
                this.model.node_info.server.server_type == 'pg' &&
                // No need to check this when creating a view
                this.model.get('oid') !== undefined
              ) || !(
                this.model.origSessAttrs &&
                this.model.changed.definition != this.model.origSessAttrs.definition
              )) {
                this.model.warn_text = undefined;
                return;
              }

              let old_def = this.model.origSessAttrs.definition &&
                this.model.origSessAttrs.definition.replace(
                  /\s/gi, ''
                ).split('FROM'),
                new_def = [];

              if (this.model.changed.definition !== undefined) {
                new_def = this.model.changed.definition.replace(
                  /\s/gi, ''
                ).split('FROM');
              }

              if ((old_def.length != new_def.length) || (
                old_def.length > 1 && (
                  old_def[0] != new_def[0]
                )
              )) {
                this.model.warn_text = gettext(
                  'Changing the columns in a view requires dropping and re-creating the view. This may fail if other objects are dependent upon this view, or may cause procedural functions to fail if they are not modified to take account of the changes.'
                ) + '<br><br><b>' + gettext('Do you wish to continue?') +
                '</b>';
              } else {
                this.model.warn_text = undefined;
              }
            },
          }),
        },
        //  pgBrowser.SecurityGroupSchema, {
        //   // Add Privilege Control
        //   id: 'datacl', label: gettext('Privileges'), type: 'collection',
        //   model: pgBrowser.Node.PrivilegeRoleModel.extend({
        //     privileges: ['a', 'r', 'w', 'd', 'D', 'x', 't'],
        //   }), uniqueCol : ['grantee'], editable: false, group: 'security',
        //   mode: ['edit', 'create'], canAdd: true, canDelete: true,
        //   control: 'unique-col-collection', disabled: 'notInSchema',
        // }
        // ,{
        //   // Add Security Labels Control
        //   id: 'seclabels', label: gettext('Security labels'),
        //   model: pgBrowser.SecLabelModel, editable: false, type: 'collection',
        //   canEdit: false, group: 'security', canDelete: true,
        //   mode: ['edit', 'create'], canAdd: true, disabled: 'notInSchema',
        //   control: 'unique-col-collection', uniqueCol : ['provider'],
        // }
      ],
        validate: function() {
          // Triggers specific error messages for fields
          var err = {},
            errmsg,
            field_name = this.get('name'),
            field_def = this.get('definition');
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
            err['definition'] = gettext('Please enter view code.');
            errmsg = errmsg || err['definition'];
            this.errorModel.set('definition', errmsg);
            return errmsg;
          }else{
            this.errorModel.unset('definition');
          }
          return null;
        },
        // We will disable everything if we are under catalog node
        notInSchema: function() {
          if(this.node_info && 'catalog' in this.node_info) {
            return true;
          }
          return false;
        },
      }),
    });
  }

  return pgBrowser.Nodes['view'];
});
