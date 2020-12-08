from config import *
import os


PROJ_ROOT = os.path.dirname(root)
DATA_DIR = os.path.join(PROJ_ROOT, 'data')
DB_DIR = os.path.join(PROJ_ROOT, 'db')
LOG_DIR = os.path.join(PROJ_ROOT, 'logs')
STORAGE_DIR = os.path.join(DATA_DIR, 'storage')
SESSION_DB_PATH = os.path.join(DATA_DIR, 'sessions')

for path in (DATA_DIR, DB_DIR, LOG_DIR, STORAGE_DIR, SESSION_DB_PATH, ):
    if not os.path.exists(path):
        os.makedirs(path)


##########################################################################
# Development Server settings L103
##########################################################################

DEFAULT_SERVER = '0.0.0.0'

# App mode if False
SERVER_MODE = True

# Enable the test module
MODULE_BLACKLIST.remove('test')

WTF_CSRF_ENABLED = False

##########################################################################
# Log settings L224
##########################################################################

# Debug mode, default False
DEBUG = True

# Application log level - one of:
#   CRITICAL 50
#   ERROR    40
#   WARNING  30
#   SQL      25
#   INFO     20
#   DEBUG    10
#   NOTSET    0
CONSOLE_LOG_LEVEL = logging.DEBUG
FILE_LOG_LEVEL = logging.DEBUG

# Log format.
# CONSOLE_LOG_FORMAT = '%(asctime)s: %(levelname)s\t%(name)s:\t%(message)s'
CONSOLE_LOG_FORMAT = '%(asctime)s: %(levelname)s\t%(name)s:\t\t%(pathname)s\t%(lineno)d\t%(message)s'
FILE_LOG_FORMAT = '%(asctime)s: %(levelname)s\t%(name)s:\t%(message)s'

# Log file name. This goes in the data directory, except on non-Windows
# platforms in server mode.
if SERVER_MODE and not IS_WIN:
    LOG_FILE = os.path.join(LOG_DIR, 'pgadmin4-server.log')
else:
    LOG_FILE = os.path.join(LOG_DIR, 'pgadmin4-desktop.log')


##########################################################################
# Server Connection Driver Settings L253
##########################################################################

# The default driver used for making connection with PostgreSQL

# -------------------------------------------------------------------------
# TODO: ACCOMDATE TO PYTHON SNOWBALL_DRIVER
# psycopg2.__libpq_version__ == 90224
# fake sversion = 90824 9.8.24
# PG_DEFAULT_DRIVER = 'psycopg2'
PG_DEFAULT_DRIVER = 'snowball'

# psycopg2.__libpq_version__
# Integer constant reporting the version of the libpq library
# this psycopg2 module was compiled with (in the same format of server_version)
# If this value is greater or equal than 90100
# then you may query the version of the actually loaded library using the libpq_version() function.


##########################################################################
# User account and settings storage L264
##########################################################################

# Use a different config DB for each server mode.
if SERVER_MODE == False:
    SQLITE_PATH = os.path.join(
        DB_DIR,
        'pgadmin4-desktop.db',
    )
else:
    SQLITE_PATH = os.path.join(
        DB_DIR,
        'pgadmin4-server.db',
    )


##########################################################################
# Upgrade checks L341
##########################################################################

UPGRADE_CHECK_ENABLED = False

##########################################################################
# External Authentication Sources L491
##########################################################################

# front-end fix session(cookie) flush on browser refresh
# $window.location.reload();
# sessionStorage.clear();
# sessionStorage.removeItem('key');


##########################################################################
# Modulles to skip LEND
##########################################################################

# snowball server currently does not support these modules.
MODULES_TO_SKIP = (
    # 'pgadmin.about',
    # 'pgadmin.authenticate',
    # 'pgadmin.authenticate.internal',
    # 'pgadmin.authenticate.ldap',
    # 'pgadmin.authenticate.registry',
    # 'pgadmin.browser',
    # 'pgadmin.browser.collection',
    # 'pgadmin.browser.register_browser_preferences',
    # 'pgadmin.browser.server_groups',
    # 'pgadmin.browser.server_groups.servers',
    # 'pgadmin.browser.server_groups.servers.databases',
    'pgadmin.browser.server_groups.servers.databases.casts',
    'pgadmin.browser.server_groups.servers.databases.casts.tests',
    'pgadmin.browser.server_groups.servers.databases.event_triggers',
    'pgadmin.browser.server_groups.servers.databases.event_triggers.tests',
    'pgadmin.browser.server_groups.servers.databases.extensions',
    'pgadmin.browser.server_groups.servers.databases.extensions.tests',
    'pgadmin.browser.server_groups.servers.databases.external_tables',
    'pgadmin.browser.server_groups.servers.databases.external_tables.actions',
    'pgadmin.browser.server_groups.servers.databases.external_tables.mapping_utils',
    'pgadmin.browser.server_groups.servers.databases.external_tables.properties',
    'pgadmin.browser.server_groups.servers.databases.external_tables.reverse_engineer_ddl',
    'pgadmin.browser.server_groups.servers.databases.external_tables.tests',
    'pgadmin.browser.server_groups.servers.databases.foreign_data_wrappers',
    'pgadmin.browser.server_groups.servers.databases.foreign_data_wrappers.foreign_servers',
    'pgadmin.browser.server_groups.servers.databases.foreign_data_wrappers.foreign_servers.tests',
    'pgadmin.browser.server_groups.servers.databases.foreign_data_wrappers.foreign_servers.user_mappings',
    'pgadmin.browser.server_groups.servers.databases.foreign_data_wrappers.foreign_servers.user_mappings.tests',
    'pgadmin.browser.server_groups.servers.databases.foreign_data_wrappers.tests',
    'pgadmin.browser.server_groups.servers.databases.languages',
    'pgadmin.browser.server_groups.servers.databases.languages.tests',
    # 'pgadmin.browser.server_groups.servers.databases.schemas',
    'pgadmin.browser.server_groups.servers.databases.schemas.catalog_objects',
    'pgadmin.browser.server_groups.servers.databases.schemas.catalog_objects.columns',
    'pgadmin.browser.server_groups.servers.databases.schemas.collations',
    'pgadmin.browser.server_groups.servers.databases.schemas.collations.tests',
    'pgadmin.browser.server_groups.servers.databases.schemas.domains',
    'pgadmin.browser.server_groups.servers.databases.schemas.domains.domain_constraints',
    'pgadmin.browser.server_groups.servers.databases.schemas.domains.tests',
    'pgadmin.browser.server_groups.servers.databases.schemas.foreign_tables',
    'pgadmin.browser.server_groups.servers.databases.schemas.foreign_tables.tests',
    'pgadmin.browser.server_groups.servers.databases.schemas.fts_configurations',
    'pgadmin.browser.server_groups.servers.databases.schemas.fts_configurations.tests',
    'pgadmin.browser.server_groups.servers.databases.schemas.fts_dictionaries',
    'pgadmin.browser.server_groups.servers.databases.schemas.fts_dictionaries.tests',
    'pgadmin.browser.server_groups.servers.databases.schemas.fts_parsers',
    'pgadmin.browser.server_groups.servers.databases.schemas.fts_parsers.tests',
    'pgadmin.browser.server_groups.servers.databases.schemas.fts_templates',
    'pgadmin.browser.server_groups.servers.databases.schemas.fts_templates.tests',
    'pgadmin.browser.server_groups.servers.databases.schemas.functions',
    'pgadmin.browser.server_groups.servers.databases.schemas.functions.tests',
    'pgadmin.browser.server_groups.servers.databases.schemas.packages',
    'pgadmin.browser.server_groups.servers.databases.schemas.packages.edbfuncs',
    'pgadmin.browser.server_groups.servers.databases.schemas.packages.edbfuncs.tests',
    'pgadmin.browser.server_groups.servers.databases.schemas.packages.edbvars',
    'pgadmin.browser.server_groups.servers.databases.schemas.packages.tests',
    'pgadmin.browser.server_groups.servers.databases.schemas.sequences',
    'pgadmin.browser.server_groups.servers.databases.schemas.sequences.tests',
    'pgadmin.browser.server_groups.servers.databases.schemas.synonyms',
    'pgadmin.browser.server_groups.servers.databases.schemas.synonyms.tests',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.base_partition_table',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.columns',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.columns.tests',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.columns.utils',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.compound_triggers',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.compound_triggers.tests',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.compound_triggers.utils',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.constraints',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.constraints.check_constraint',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.constraints.check_constraint.tests',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.constraints.check_constraint.utils',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.constraints.exclusion_constraint',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.constraints.foreign_key',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.constraints.index_constraint',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.constraints.tests',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.constraints.type',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.indexes',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.indexes.tests',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.indexes.utils',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.partitions',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.partitions.tests',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.rules',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.rules.tests',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.schema_diff_utils',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.tests',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.triggers',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.triggers.tests',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.triggers.utils',
    # 'pgadmin.browser.server_groups.servers.databases.schemas.tables.utils',
    'pgadmin.browser.server_groups.servers.databases.schemas.tests',
    'pgadmin.browser.server_groups.servers.databases.schemas.types',
    'pgadmin.browser.server_groups.servers.databases.schemas.types.tests',
    'pgadmin.browser.server_groups.servers.databases.schemas.utils',
    'pgadmin.browser.server_groups.servers.databases.schemas.views',
    'pgadmin.browser.server_groups.servers.databases.schemas.views.children',
    'pgadmin.browser.server_groups.servers.databases.schemas.views.tests',
    'pgadmin.browser.server_groups.servers.databases.tests',
    'pgadmin.browser.server_groups.servers.databases.utils',
    # 'pgadmin.browser.server_groups.servers.gpdb',
    'pgadmin.browser.server_groups.servers.pgagent',
    'pgadmin.browser.server_groups.servers.pgagent.schedules',
    'pgadmin.browser.server_groups.servers.pgagent.steps',
    'pgadmin.browser.server_groups.servers.pgagent.tests',
    'pgadmin.browser.server_groups.servers.pgagent.utils',
    # 'pgadmin.browser.server_groups.servers.ppas',
    # 'pgadmin.browser.server_groups.servers.resource_groups',
    # 'pgadmin.browser.server_groups.servers.resource_groups.tests',
    'pgadmin.browser.server_groups.servers.roles',
    'pgadmin.browser.server_groups.servers.roles.tests',
    'pgadmin.browser.server_groups.servers.tablespaces',
    'pgadmin.browser.server_groups.servers.tablespaces.tests',
    # 'pgadmin.browser.server_groups.servers.tests',
    # 'pgadmin.browser.server_groups.servers.types',
    # 'pgadmin.browser.server_groups.servers.utils',
    # 'pgadmin.browser.server_groups.tests',
    # 'pgadmin.browser.tests',
    # 'pgadmin.browser.utils',
    # 'pgadmin.dashboard',
    # 'pgadmin.dashboard.tests',
    # 'pgadmin.feature_tests',
    # 'pgadmin.help',
    # 'pgadmin.misc',
    # 'pgadmin.misc.bgprocess',
    # 'pgadmin.misc.bgprocess.process_executor',
    # 'pgadmin.misc.bgprocess.processes',
    # 'pgadmin.misc.dependencies',
    # 'pgadmin.misc.dependents',
    # 'pgadmin.misc.file_manager',
    # 'pgadmin.misc.sql',
    # 'pgadmin.misc.statistics',
    # 'pgadmin.misc.themes',
    # 'pgadmin.model',
    # 'pgadmin.preferences',
    # 'pgadmin.redirects',
    # 'pgadmin.settings',
    # 'pgadmin.setup',
    # 'pgadmin.tools',
    # 'pgadmin.tools.backup',
    # 'pgadmin.tools.backup.tests',
    # 'pgadmin.tools.datagrid',
    # 'pgadmin.tools.debugger',
    # 'pgadmin.tools.debugger.utils',
    # 'pgadmin.tools.grant_wizard',
    # 'pgadmin.tools.import_export',
    # 'pgadmin.tools.import_export.tests',
    # 'pgadmin.tools.maintenance',
    # 'pgadmin.tools.maintenance.tests',
    # 'pgadmin.tools.restore',
    # 'pgadmin.tools.restore.tests',
    # 'pgadmin.tools.schema_diff',
    # 'pgadmin.tools.schema_diff.compare',
    # 'pgadmin.tools.schema_diff.directory_compare',
    # 'pgadmin.tools.schema_diff.model',
    # 'pgadmin.tools.schema_diff.node_registry',
    # 'pgadmin.tools.schema_diff.tests',
    # 'pgadmin.tools.search_objects',
    # 'pgadmin.tools.search_objects.tests',
    # 'pgadmin.tools.search_objects.utils',
    # 'pgadmin.tools.sqleditor',
    # 'pgadmin.tools.sqleditor.command',
    # 'pgadmin.tools.sqleditor.tests',
    # 'pgadmin.tools.sqleditor.utils',
    # 'pgadmin.tools.user_management',
    # 'pgadmin.utils',
)
