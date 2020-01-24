#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

logger = __import__('logging').getLogger(__name__)


try:
    from sqlalchemy.dialects.mysql.mysqldb import MySQLDialect_mysqldb
    from relstorage.adapters.mysql.drivers.mysqldb import GeventMySQLdbDriver
except ImportError:
    pass
else:
    class geventMysqlclient_dialect(MySQLDialect_mysqldb):
        driver = "gevent+mysql"

        def __init__(self, *args, **kwargs):
            super(geventMysqlclient_dialect, self).__init__(*args, **kwargs)
            self.connect = GeventMySQLdbDriver().connect

    from sqlalchemy.dialects import registry
    registry.register("gevent.mysql", __name__, "geventMysqlclient_dialect")


try:
    from sqlalchemy.dialects.sqlite.pysqlite import SQLiteDialect_pysqlite
    from relstorage.adapters.sqlite.drivers import Sqlite3GeventDriver
except ImportError:
    pass
else:
    class geventSqliteclient_dialect(SQLiteDialect_pysqlite):
        driver = "gevent+sqlite"

        def __init__(self, *args, **kwargs):
            super(geventSqliteclient_dialect, self).__init__(*args, **kwargs)
            self.connect = Sqlite3GeventDriver().connect_to_file

    from sqlalchemy.dialects import registry
    registry.register("gevent.sqlite", __name__, geventSqliteclient_dialect.__name__)


def patch_retryable():
    # Duplicate entry mysqlclient/sqlite IntegrityErrors should be retryable
    from MySQLdb import IntegrityError
    import zope.sqlalchemy.datamanager as sdm
    sdm._retryable_errors.append((IntegrityError, lambda e: e.args[0] == 1062))

    from sqlite3 import OperationalError
    from sqlite3 import IntegrityError as sqlite_IntegrityError
    sdm._retryable_errors.append((sqlite_IntegrityError,
                                  lambda e: e.args[0].lower().startswith('unique constraint failed')))
    sdm._retryable_errors.append((OperationalError,
                                  lambda e: e.args[0].lower().startswith('database is locked')))

def patch():
    patch_retryable()
