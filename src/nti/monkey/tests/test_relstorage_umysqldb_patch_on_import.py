#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""


$Id$
"""

from __future__ import print_function, unicode_literals, absolute_import
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

#disable: accessing protected members, too many methods
#pylint: disable=W0212,R0904

import unittest
from hamcrest import assert_that
from hamcrest import is_

from nti.testing.matchers import is_true
from nti.testing.matchers import is_false

class TestPatch(unittest.TestCase):

	def test_timestamp_to_tid_patch(self):
		import nti.monkey.relstorage_umysqldb_patch_on_import
		nti.monkey.relstorage_umysqldb_patch_on_import.patch()

		from relstorage.storage import RelStorage

		class Adapter(object):
			pass

		class Schema(object):
			def prepare(self): pass

		class Locker(object):
			def hold_commit_lock( self, cursor, ensure_current=True ):
				pass

		class TxnControl(object):
			last_tid = 1
			def get_tid( self, cursor ):
				return self.last_tid
			def add_transaction( self, cursor, tid_int, user, desc, ext ):
				pass

		adapter = Adapter()
		adapter.schema = Schema()
		adapter.txncontrol = TxnControl()
		adapter.locker = Locker()

		storage = RelStorage( adapter )
		storage._transaction = object()
		storage._ude = (None, None, None)

		storage._prepare_tid()

		assert_that( storage._tid, is_( bytes ) ) # bytes, not unicode


	def test_sqlalchemy_retry(self):
		import nti.monkey.relstorage_umysqldb_patch_on_import
		nti.monkey.relstorage_umysqldb_patch_on_import.patch()

		from zope.sqlalchemy.datamanager import SessionDataManager
		import transaction
		import pymysql.err
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
		manager = SessionDataManager(MockSession(), 'status', transaction.manager)

		exc = pymysql.err.OperationalError()
		sql_exc = sqlalchemy.exc.OperationalError('statement', 'params', exc)
		assert_that( transaction.manager._retryable(type(sql_exc), sql_exc),
					 is_true() )

		transaction.abort()
		del manager

		# Without being in a transaction, the manager gives us False
		assert_that( transaction.manager._retryable(type(sql_exc), sql_exc),
					 is_false() )

		# But the transaction loop has been batched to recognize this
		# even outside a ZopeTransactionExtension

		from nti.utils.transactions import TransactionLoop
		assert_that( TransactionLoop._retryable.im_func(TransactionLoop,  (type(sql_exc), sql_exc, None) ),
					 is_true() )
