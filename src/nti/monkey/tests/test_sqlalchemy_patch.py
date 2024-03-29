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

from nose.tools import assert_raises

import os
import tempfile
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

        def do_test(root_exception, is_retryable=True):
            # This joins the session to the transaction manager
            manager = SessionDataManager(MockSession(),
                                         'status',
                                         transaction.manager)

            sql_exc = sqlalchemy.exc.IntegrityError('statement', 'params', root_exception)
            assert_that(transaction.manager.get().isRetryableError(sql_exc),
                        is_(is_retryable))

            transaction.abort()
            del manager

            # Without being in a transaction, the manager gives us False
            assert_that(transaction.manager.get().isRetryableError(sql_exc),
                        is_(False))

        from MySQLdb import IntegrityError
        retryable_exc = IntegrityError(1062, 'Duplicate error')
        do_test(retryable_exc)
        nonretryable_exc = IntegrityError(9999, 'Duplicate error')
        do_test(nonretryable_exc, is_retryable=False)

        # Sqlite
        import sqlite3
        from sqlite3 import OperationalError
        from sqlite3 import IntegrityError as sqlite_IntegrityError
        db_file = tempfile.mkstemp()[1]
        con1 = sqlite3.connect(db_file)
        con2 = sqlite3.connect(db_file)
        con2.execute('PRAGMA busy_timeout=1')
        try:
            con1.execute('CREATE TABLE TestRetry(id TEXT UNIQUE)')
            con1.execute('INSERT INTO TestRetry (id) VALUES ("key_val")')

            # Duplicate entry raises IntegrityError
            with assert_raises(sqlite_IntegrityError) as exception_context:
                con1.execute('INSERT INTO TestRetry (id) VALUES ("key_val")')
            retryable_exc = exception_context.exception
            do_test(retryable_exc)

            # Second connection attempts to execute while con1 has the lock
            with assert_raises(OperationalError) as exception_context:
                con2.execute('INSERT INTO TestRetry (id) VALUES ("key_val")')
            retryable_exc = exception_context.exception
            do_test(retryable_exc)
        finally:
            con1.close()
            con2.close()
            os.remove(db_file)

        nonretryable_exc = sqlite_IntegrityError('This is not retryable')
        do_test(nonretryable_exc, is_retryable=False)

        nonretryable_exc = OperationalError('This is not retryable')
        do_test(nonretryable_exc, is_retryable=False)
