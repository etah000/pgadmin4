/////////////////////////////////////////////////////////////
//
// pgAdmin 4 - PostgreSQL Tools
//
// Copyright (C) 2013 - 2020, The pgAdmin Development Team
// This software is released under the PostgreSQL Licence
//
//////////////////////////////////////////////////////////////

define('pgadmin.node.database', [
  'sources/gettext', 'sources/url_for', 'jquery', 'underscore',
  'sources/utils', 'sources/pgadmin', 'pgadmin.browser.utils',
  'pgadmin.alertifyjs', 'pgadmin.backform', 'pgadmin.browser.collection',
  'pgadmin.browser.server.privilege', 'pgadmin.browser.server.variable',
], function(gettext, url_for, $, _, pgadminUtils, pgAdmin, pgBrowser, Alertify, Backform) {

  if (!pgBrowser.Nodes['coll-database']) {
    pgBrowser.Nodes['coll-database'] =
      pgBrowser.Collection.extend({
        node: 'database',
        label: gettext('Databases'),
        type: 'coll-database',
        columns: ['name', 'engine', 'data_path', 'metadata_path'],
        hasStatistics: true,
        canDrop: true,
        canDropCascade: false,
        statsPrettifyFields: [gettext('Size'), gettext('Size of temporary files')],
      });
  }

  if (!pgBrowser.Nodes['database']) {
    pgBrowser.Nodes['database'] = pgBrowser.Node.extend({
      parent_type: 'server',
      type: 'database',
      width: '250px',
      height: '250px',
      sqlAlterHelp: 'sql-alterdatabase.html',
      sqlCreateHelp: 'sql-createdatabase.html',
      dialogHelp: url_for('help.static', {'filename': 'database_dialog.html'}),
      hasSQL: true,
      canEdit: true,
      hasDepends: true,
      hasStatistics: true,
      statsPrettifyFields: [gettext('Size'), gettext('Size of temporary files')],
      canDrop: function(node) {
        return node.canDrop;
      },
      label: gettext('Database'),
      node_image: function() {
        return 'pg-icon-database';
      },
      Init: function() {
        /* Avoid mulitple registration of menus */
        if (this.initialized)
          return;

        this.initialized = true;

        pgBrowser.add_menus([
        {
          name: 'create_database_on_server', node: 'server', module: this,
          applies: ['object', 'context'], callback: 'show_obj_properties',
          category: 'create', priority: 4, label: gettext('Database...'),
          icon: 'wcTabIcon pg-icon-database', data: {action: 'create'},
          enable: false,
        },
        // {
        //   name: 'create_database_on_coll', node: 'coll-database', module: this,
        //   applies: ['object', 'context'], callback: 'show_obj_properties',
        //   category: 'create', priority: 4, label: gettext('Database...'),
        //   icon: 'wcTabIcon pg-icon-database', data: {action: 'create'},
        //   enable: 'can_create_database',
        // },
        {
          name: 'create_database', node: 'coll-database', module: this,
          applies: ['object', 'context'], callback: 'show_obj_properties',
          category: 'create', priority: 4, label: gettext('Database...'),
          icon: 'wcTabIcon pg-icon-database', data: {action: 'create'},
        },
        // {
        //   name: 'create_database', node: 'database', module: this,
        //   applies: ['object', 'context'], callback: 'show_obj_properties',
        //   category: 'create', priority: 4, label: gettext('Database...'),
        //   icon: 'wcTabIcon pg-icon-database', data: {action: 'create'},
        //   enable: 'can_create_database',
        // },
        // {
        //   name: 'connect_database', node: 'database', module: this,
        //   applies: ['object', 'context'], callback: 'connect_database',
        //   category: 'connect', priority: 4, label: gettext('Connect Database...'),
        //   icon: 'fa fa-link', enable : 'is_not_connected',
        // }
        // ,{
        //   name: 'disconnect_database', node: 'database', module: this,
        //   applies: ['object', 'context'], callback: 'disconnect_database',
        //   category: 'drop', priority: 5, label: gettext('Disconnect Database...'),
        //   icon: 'fa fa-chain-broken', enable : 'is_connected',
        // }
      ]);

        _.bindAll(this, 'connection_lost');
        pgBrowser.Events.on(
          'pgadmin:database:connection:lost', this.connection_lost
        );
      },
      can_create_database: function(node, item) {
        var treeData = this.getTreeNodeHierarchy(item),
          server = treeData['server'];

        return server.connected && server.user.can_create_db;
      },
      is_not_connected: function(node) {
        return (node && node.connected != true && node.allowConn == true);
      },
      is_connected: function(node) {
        return (node && node.connected == true && node.canDisconn == true);
      },
      is_conn_allow: function(node) {
        return (node && node.allowConn == true);
      },
      connection_lost: function(i, resp, server_connected) {
        if (pgBrowser.tree) {
          var t = pgBrowser.tree,
            d = i && t.itemData(i),
            self = this;

          while (d && d._type != 'database') {
            i = t.parent(i);
            d = i && t.itemData(i);
          }

          if (i && d) {
            if (!d.allowConn) return false;
            if (_.isUndefined(d.is_connecting) || !d.is_connecting) {
              d.is_connecting = true;

              var disconnect = function(_i, _d) {
                if (_d._id == this._id) {
                  d.is_connecting = false;
                  pgBrowser.Events.off(
                    'pgadmin:database:connect:cancelled', disconnect
                  );
                  _i = _i && t.parent(_i);
                  _d = _i && t.itemData(_i);
                  if (_i && _d) {
                    pgBrowser.Events.trigger(
                      'pgadmin:server:disconnect',
                      {item: _i, data: _d}, false
                    );
                  }
                }
              };

              pgBrowser.Events.on(
                'pgadmin:database:connect:cancelled', disconnect
              );
              if (server_connected) {
                connect(self, d, t, i, true);
                return;
              }
              Alertify.confirm(
                gettext('Connection lost'),
                gettext('Would you like to reconnect to the database?'),
                function() {
                  connect(self, d, t, i, true);
                },
                function() {
                  d.is_connecting = false;
                  t.unload(i);
                  t.setInode(i);
                  t.addIcon(i, {icon: 'icon-database-not-connected'});
                  pgBrowser.Events.trigger(
                    'pgadmin:database:connect:cancelled', i, d, self
                  );
                });
            }
          }
        }
      },
      callbacks: {
        /* Connect the database */
        connect_database: function(args){
          var input = args || {},
            obj = this,
            t = pgBrowser.tree,
            i = input.item || t.selected(),
            d = i && i.length == 1 ? t.itemData(i) : undefined;

          if (!d || d.label == 'template0')
            return false;

          connect_to_database(obj, d, t, i, true);
          return false;
        },
        /* Disconnect the database */
        disconnect_database: function(args) {
          var input = args || {},
            obj = this,
            t = pgBrowser.tree,
            i = input.item || t.selected(),
            d = i && i.length == 1 ? t.itemData(i) : undefined;

          if (!d)
            return false;

          Alertify.confirm(
            gettext('Disconnect the database'),
            gettext('Are you sure you want to disconnect the database - %s?', d.label),
            function() {
              var data = d;
              $.ajax({
                url: obj.generate_url(i, 'connect', d, true),
                type:'DELETE',
              })
                .done(function(res) {
                  if (res.success == 1) {
                    var prv_i = t.parent(i);
                    if(res.data.info_prefix) {
                      res.info = `${_.escape(res.data.info_prefix)} - ${res.info}`;
                    }
                    Alertify.success(res.info);
                    t.removeIcon(i);
                    data.connected = false;
                    data.icon = 'icon-database-not-connected';
                    t.addIcon(i, {icon: data.icon});
                    t.unload(i);
                    t.setInode(i);
                    setTimeout(function() {
                      t.select(prv_i);
                    }, 10);

                  } else {
                    try {
                      Alertify.error(res.errormsg);
                    } catch (e) {
                      console.warn(e.stack || e);
                    }
                    t.unload(i);
                  }
                })
                .fail(function(xhr, status, error) {
                  Alertify.pgRespErrorNotify(xhr, error);
                  t.unload(i);
                });
            },
            function() { return true; }
          ).set('labels', {
            ok: gettext('Yes'),
            cancel: gettext('No'),
          });

          return false;
        },

        /* Connect the database (if not connected), before opening this node */
        beforeopen: function(item, data) {
          if(!data || data._type != 'database' || data.label == 'template0') {
            return false;
          }
          pgBrowser.tree.addIcon(item, {icon: data.icon});
          if (!data.connected && data.allowConn) {
            connect_to_database(this, data, pgBrowser.tree, item, true);
            return false;
          }
          return true;
        },

        selected: function(item, data) {
          if(!data || data._type != 'database') {
            return false;
          }

          pgBrowser.tree.addIcon(item, {icon: data.icon});
          if (!data.connected && data.allowConn) {
            connect_to_database(this, data, pgBrowser.tree, item, false);
            return false;
          }

          return pgBrowser.Node.callbacks.selected.apply(this, arguments);
        },

        refresh: function(cmd, i) {
          var t = pgBrowser.tree,
            item = i || t.selected(),
            d = t.itemData(item);

          if (!d.allowConn) return;
          pgBrowser.Node.callbacks.refresh.apply(this, arguments);
        },
      },
      model: pgBrowser.Node.Model.extend({
        idAttribute: 'did',
        defaults: {
          name: undefined,
          cluster: undefined,
          engine: undefined,
          data_path: undefined,
          metadata_path: undefined,
          // owner: undefined,
          // is_sys_obj: undefined,
          // comment: undefined,
          // encoding: 'UTF8',
          // template: undefined,
          // tablespace: undefined,
          // collation: undefined,
          // char_type: undefined,
          // datconnlimit: -1,
          // datallowconn: undefined,
          // variables: [],
          // privileges: [],
          // securities: [],
          // datacl: [],
          // deftblacl: [],
          // deffuncacl: [],
          // defseqacl: [],
          // is_template: false,
          // deftypeacl: [],
        },

        // Default values!
        initialize: function(attrs, args) {
          var isNew = (_.size(attrs) === 0);

          if (isNew) {
            var userInfo = pgBrowser.serverInfo[args.node_info.server._id].user;
            this.set({'datowner': userInfo.name}, {silent: true});
          }
          pgBrowser.Node.Model.prototype.initialize.apply(this, arguments);
        },

        schema: [{
          id: 'name', label: gettext('Database'), cell: 'string',
          editable: false, type: 'text',
        },
        // {
        //   id: 'engine', label: gettext('Engine'), cell: 'string',
        //   editable: false, type: 'text',disabled:true,
        // },
        // {
        //   id: 'data_path', label: gettext('Data Path'), cell: 'string',
        //   editable: false, type: 'text',disabled:true,
        // },
        {
          id: 'cluster', label: gettext('On Cluster'), type: 'text', node: 'cluster',
          select2: {allowClear: true}, control: 'node-list-by-name', editable: false,
          mode: ['edit', 'create'],
        },
        // {
        //   id: 'metadata_path', label: gettext('Metadata Path'), cell: 'string',
        //   editable: false, type: 'text',disabled:true,
        // },
        ],
        validate: function() {
          var name = this.get('name');
          if (_.isUndefined(name) || _.isNull(name) ||
            String(name).replace(/^\s+|\s+$/g, '') == '') {
            var msg = gettext('Name cannot be empty.');
            this.errorModel.set('name', msg);
            return msg;
          } else {
            this.errorModel.unset('name');
          }
          return null;
        },
      }),
    });


    pgBrowser.SecurityGroupSchema = {
      id: 'security', label: gettext('Security'), type: 'group',
      // Show/Hide security group for nodes under the catalog
      visible: function(args) {
        if (args && 'node_info' in args) {
          // If node_info is not present in current object then it might in its
          // parent in case if we used sub node control
          var node_info = args.node_info || args.handler.node_info;
          return 'catalog' in node_info ? false : true;
        }
        return true;
      },
    };

    var connect_to_database = function(obj, data, tree, item) {
        connect(obj, data, tree, item);
      },
      connect = function (obj, data, tree, item, _wasConnected) {
        var wasConnected = _wasConnected || data.connected,
          onFailure = function(
            xhr, status, error, _model, _data, _tree, _item, _status
          ) {
            if (!_status) {
              tree.setInode(_item);
              tree.addIcon(_item, {icon: 'icon-database-not-connected'});
            }

            Alertify.pgNotifier('error', xhr, error, function(msg) {
              setTimeout(function() {
                if (msg == 'CRYPTKEY_SET') {
                  connect_to_database(_model, _data, _tree, _item, _wasConnected);
                } else {
                  Alertify.dlgServerPass(
                    gettext('Connect to database'),
                    msg, _model, _data, _tree, _item, _status,
                    onSuccess, onFailure, onCancel
                  ).resizeTo();
                }
              }, 100);
            });
          },
          onSuccess = function(
            res, model, data, tree, item, connected
          ) {
            data.is_connecting = false;
            if (!connected) {
              tree.deselect(item);
              tree.setInode(item);
            }
            if (res && res.data) {
              if(typeof res.data.connected == 'boolean') {
                data.connected = res.data.connected;
              }
              if (typeof res.data.icon == 'string') {
                tree.removeIcon(item);
                data.icon = res.data.icon;
                tree.addIcon(item, {icon: data.icon});
              }
              if(res.data.already_connected) {
                res.info = gettext('Database already connected.');
              }
              if(res.data.info_prefix) {
                res.info = `${_.escape(res.data.info_prefix)} - ${res.info}`;
              }
              if(res.data.already_connected) {
                Alertify.info(res.info);
              } else {
                Alertify.success(res.info);
              }
              obj.trigger('connected', obj, item, data);
              pgBrowser.Events.trigger(
                'pgadmin:database:connected', item, data
              );

              if (!connected) {
                setTimeout(function() {
                  tree.select(item);
                  tree.open(item);
                }, 10);
              }
            }
          },
          onCancel = function(_tree, _item, _data) {
            _data.is_connecting = false;
            var server = _tree.parent(_item);
            _tree.unload(_item);
            _tree.setInode(_item);
            _tree.removeIcon(_item);
            _tree.addIcon(_item, {icon: 'icon-database-not-connected'});
            obj.trigger('connect:cancelled', obj, _item, _data);
            pgBrowser.Events.trigger(
              'pgadmin:database:connect:cancelled', _item, _data, obj
            );
            _tree.select(server);
          };

        $.post(
          obj.generate_url(item, 'connect', data, true)
        ).done(function(res) {
          if (res.success == 1) {
            return onSuccess(res, obj, data, tree, item, wasConnected);
          }
        }).fail(function(xhr, status, error) {
          if (xhr.status === 410) {
            error = gettext('Error: Object not found - %s.', error);
          }
          return onFailure(
            xhr, status, error, obj, data, tree, item, wasConnected
          );
        });
      };
  }

  return pgBrowser.Nodes['coll-database'];
});
