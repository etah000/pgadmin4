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

if True:
    from modules_active import MODULES_ACTIVE
