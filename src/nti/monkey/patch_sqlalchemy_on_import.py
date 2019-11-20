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
            logger.info('..............................using relstorage drive')
            super(geventSqliteclient_dialect, self).__init__(*args, **kwargs)
            self.connect = Sqlite3GeventDriver().connect

    from sqlalchemy.dialects import registry
    registry.register("gevent.sqlite", __name__, "geventSqliteclient_dialect")


def patch():
    pass
