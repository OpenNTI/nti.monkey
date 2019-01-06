#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that

import unittest


class TestPatch(unittest.TestCase):

    def test_timestamp_to_tid_patch(self):
        import nti.monkey.patch_relstorage_umysqldb_on_import
        nti.monkey.patch_relstorage_umysqldb_on_import.patch()

        from relstorage.storage import RelStorage

        class Adapter(object):
            packundo = None

        class Schema(object):

            def prepare(self): pass

            def get_database_name(self, cursor):
                return ''

        class Locker(object):

            def hold_commit_lock(self, cursor, ensure_current=True):
                pass

        class TxnControl(object):
            last_tid = 1

            def get_tid(self, cursor):
                return self.last_tid

            def add_transaction(self, cursor, tid_int, user, desc, ext):
                pass

        class ConnManager(object):

            def open_for_load(self):
                return None, None

            def close(self, conn, cursor):
                pass

        adapter = Adapter()
        adapter.schema = Schema()
        adapter.txncontrol = TxnControl()
        adapter.locker = Locker()
        adapter.connmanager = ConnManager()

        storage = RelStorage(adapter)
        storage._transaction = object()
        storage._ude = (None, None, None)

        storage._prepare_tid()

        assert_that(storage._tid, is_(bytes))  # bytes, not unicode

