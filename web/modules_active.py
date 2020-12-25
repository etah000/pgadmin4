
# only active modules will be loaded for development

MODULES_ACTIVE = (
    'pgadmin.about',
    'pgadmin.authenticate',
    'pgadmin.authenticate.internal',
    'pgadmin.authenticate.ldap',
    'pgadmin.authenticate.registry',
    'pgadmin.browser',
    'pgadmin.browser.collection',
    'pgadmin.browser.register_browser_preferences',
    'pgadmin.browser.server_groups',
    'pgadmin.browser.server_groups.servers',
    # 'pgadmin.browser.server_groups.servers.clusters',
    'pgadmin.browser.server_groups.servers.databases',
    # 'pgadmin.browser.server_groups.servers.databases.casts',
    # 'pgadmin.browser.server_groups.servers.databases.event_triggers',
    # 'pgadmin.browser.server_groups.servers.databases.extensions',
    # 'pgadmin.browser.server_groups.servers.databases.external_tables',
    # 'pgadmin.browser.server_groups.servers.databases.external_tables.actions',
    # 'pgadmin.browser.server_groups.servers.databases.external_tables.mapping_utils',
    # 'pgadmin.browser.server_groups.servers.databases.external_tables.properties',
    # 'pgadmin.browser.server_groups.servers.databases.external_tables.reverse_engineer_ddl',
    # 'pgadmin.browser.server_groups.servers.databases.foreign_data_wrappers',
    # 'pgadmin.browser.server_groups.servers.databases.foreign_data_wrappers.foreign_servers',
    # 'pgadmin.browser.server_groups.servers.databases.foreign_data_wrappers.foreign_servers.user_mappings',
    # 'pgadmin.browser.server_groups.servers.databases.languages',
    'pgadmin.browser.server_groups.servers.databases.schemas',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.catalog_objects',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.catalog_objects.columns',
    'pgadmin.browser.server_groups.servers.databases.schemas.collations',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.domains',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.domains.domain_constraints',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.foreign_tables',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.fts_configurations',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.fts_dictionaries',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.fts_parsers',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.fts_templates',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.functions',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.packages',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.packages.edbfuncs',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.packages.edbvars',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.sequences',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.synonyms',
    'pgadmin.browser.server_groups.servers.databases.schemas.tables',
    'pgadmin.browser.server_groups.servers.databases.schemas.tables.base_partition_table',
    'pgadmin.browser.server_groups.servers.databases.schemas.tables.columns',
    'pgadmin.browser.server_groups.servers.databases.schemas.tables.columns.utils',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.compound_triggers',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.compound_triggers.utils',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.constraints',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.constraints.check_constraint',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.constraints.check_constraint.utils',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.constraints.exclusion_constraint',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.constraints.foreign_key',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.constraints.index_constraint',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.constraints.type',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.indexes',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.indexes.utils',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.partitions',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.rules',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.schema_diff_utils',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.triggers',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.triggers.utils',
    'pgadmin.browser.server_groups.servers.databases.schemas.tables.utils',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.types',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.utils',
    'pgadmin.browser.server_groups.servers.databases.schemas.views',
    'pgadmin.browser.server_groups.servers.databases.schemas.views.children',
    # 'pgadmin.browser.server_groups.servers.databases.utils',
    # 'pgadmin.browser.server_groups.servers.gpdb',
    # 'pgadmin.browser.server_groups.servers.pgagent',
    # 'pgadmin.browser.server_groups.servers.pgagent.schedules',
    # 'pgadmin.browser.server_groups.servers.pgagent.steps',
    # 'pgadmin.browser.server_groups.servers.pgagent.utils',
    # 'pgadmin.browser.server_groups.servers.ppas',
    # 'pgadmin.browser.server_groups.servers.resource_groups',
    'pgadmin.browser.server_groups.servers.roles',
    'pgadmin.browser.server_groups.servers.tablespaces',
    'pgadmin.browser.server_groups.servers.formats',
    'pgadmin.browser.server_groups.servers.dictionaries',
    'pgadmin.browser.server_groups.servers.datatypes',
    'pgadmin.browser.server_groups.servers.functions',
    # 'pgadmin.browser.server_groups.servers.types',
    'pgadmin.browser.server_groups.servers.utils',
    'pgadmin.browser.utils',
    'pgadmin.dashboard',
    'pgadmin.help',
    'pgadmin.misc',
    'pgadmin.misc.bgprocess',
    'pgadmin.misc.bgprocess.process_executor',
    'pgadmin.misc.bgprocess.processes',
    'pgadmin.misc.dependencies',
    'pgadmin.misc.dependents',
    'pgadmin.misc.file_manager',
    'pgadmin.misc.sql',
    'pgadmin.misc.statistics',
    'pgadmin.misc.themes',
    'pgadmin.model',
    'pgadmin.preferences',
    'pgadmin.redirects',
    'pgadmin.settings',
    'pgadmin.setup',
    'pgadmin.tools',
    'pgadmin.tools.backup',
    'pgadmin.tools.datagrid',
    'pgadmin.tools.debugger',
    'pgadmin.tools.debugger.utils',
    'pgadmin.tools.grant_wizard',
    'pgadmin.tools.import_export',
    'pgadmin.tools.maintenance',
    'pgadmin.tools.restore',
    'pgadmin.tools.schema_diff',
    'pgadmin.tools.schema_diff.compare',
    'pgadmin.tools.schema_diff.directory_compare',
    'pgadmin.tools.schema_diff.model',
    'pgadmin.tools.schema_diff.node_registry',
    'pgadmin.tools.search_objects',
    'pgadmin.tools.search_objects.utils',
    'pgadmin.tools.sqleditor',
    'pgadmin.tools.sqleditor.command',
    'pgadmin.tools.sqleditor.utils',
    'pgadmin.tools.user_management',
    'pgadmin.utils',
)
