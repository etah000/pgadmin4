from snowball_driver.dbapi.connection import Connection as _connection
from .cursor import DictCursor as Cursor

# overload snowball_driver official Connection class
# to supports DictCursor

__version__ = 0
__libpq_version__ = 0

class Connection(_connection):
    def cursor(self):
        """
        :return: a new Cursor Object using the connection.
        """
        if self.is_closed:
            raise InterfaceError('connection already closed')

        client = self._make_client()
        cursor = Cursor(client)
        self.cursors.append(cursor)

        return cursor


def connect(dsn=None, user=None, password=None, host=None, port=None,
            database=None, **kwargs):
    """
    Create a new database connection.

    The connection parameters can be specified via DSN:

        ``conn = clickhouse_driver.connect("clickhouse://localhost/test")``

    or using database and credentials arguments:

        ``conn = clickhouse_driver.connect(database="test", user="default",
        password="default", host="localhost")``

    The basic connection parameters are:

    - *host*: host with running ClickHouse server.
    - *port*: port ClickHouse server is bound to.
    - *database*: database connect to.
    - *user*: database user.
    - *password*: user's password.

    See defaults in :data:`~clickhouse_driver.connection.Connection`
    constructor.

    DSN or host is required.

    Any other keyword parameter will be passed to the underlying Connection
    class.

    :return: a new connection.
    """

    if dsn is None and host is None:
        raise ValueError('host or dsn is required')

    return Connection(dsn=dsn, user=user, password=password, host=host,
                      port=port, database=database, **kwargs)
