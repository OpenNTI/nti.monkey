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
        driver = "gevent_mysql"

        def __init__(self, *args, **kwargs):
            super(geventMysqlclient_dialect, self).__init__(*args, **kwargs)
            self.connect = GeventMySQLdbDriver().connect

    from sqlalchemy.dialects import registry
    registry.register("gevent_mysql", "nti.monkey.patch_sqlalchemy_on_import", "geventMysqlclient_dialect")


def patch():
    pass
