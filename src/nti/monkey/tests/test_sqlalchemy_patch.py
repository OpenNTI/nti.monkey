#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from hamcrest import is_
from hamcrest import none
from hamcrest import not_none
from hamcrest import assert_that
from hamcrest import instance_of

import unittest

from sqlalchemy import create_engine

from nti.monkey.patch_sqlalchemy_on_import import geventMysqlclient_dialect
from nti.monkey.patch_sqlalchemy_on_import import geventSqliteclient_dialect


class TestPatch(unittest.TestCase):

    def test_mysql_patch(self):
        from nti.monkey.patch_sqlalchemy_on_import import patch
        patch()
        engine = create_engine('gevent+mysql:///testdb.db')
        assert_that(engine, not_none())
        assert_that(engine.dialect, instance_of(geventMysqlclient_dialect))


    def test_sqlite_patch(self):
        from nti.monkey.patch_sqlalchemy_on_import import patch
        patch()
        engine = create_engine('gevent+sqlite:///testdb.db')
        assert_that(engine, not_none())
        assert_that(engine.dialect, instance_of(geventSqliteclient_dialect))

        con = engine.connect()
        sqlite_con = con.connection.connection
        assert_that(sqlite_con.isolation_level, none())
        rows = sqlite_con.execute('pragma journal_mode').fetchall()
        mode, = rows[0]
        assert_that(mode, is_('wal'))

    def test_sqlalchemy_retry(self):
        from nti.monkey.patch_sqlalchemy_on_import import patch
        patch()

        from zope.sqlalchemy.datamanager import SessionDataManager
        import transaction
        from MySQLdb import IntegrityError
        import sqlalchemy.exc

        class MockSqlTransaction(object):

            def _iterate_parents(self):
                return [transaction.get()]

        class MockSession(object):

            @property
            def transaction(self):
                return MockSqlTransaction()

            def close(self):
                pass

        # This joins the session to the transaction manager
        manager = SessionDataManager(MockSession(),
                                     'status',
                                     transaction.manager)

        retryable_exc = IntegrityError(1062, 'Duplicate error')
        sql_exc = sqlalchemy.exc.IntegrityError('statement', 'params', retryable_exc)
        assert_that(transaction.manager.get().isRetryableError(sql_exc),
                    is_(True))

        transaction.abort()
        del manager

        # Without being in a transaction, the manager gives us False
        assert_that(transaction.manager.get().isRetryableError(sql_exc),
                    is_(False))

        nonretryable_exc = IntegrityError(9999, 'Duplicate error')
        sql_exc = sqlalchemy.exc.IntegrityError('statement', 'params', nonretryable_exc)
        assert_that(transaction.manager.get().isRetryableError(sql_exc),
                    is_(False))
