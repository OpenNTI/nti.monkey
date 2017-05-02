#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Monkey-patch for RelStorage to not use subqueries. Our older mysql version
    (5.5.*) ends up not using the index and does a full-table scan. This is
    still an issue as-of mysql 5.7.17.

    https://github.com/zodb/relstorage/issues/175

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import pkg_resources

from relstorage.iter import fetchmany

rel_dist = pkg_resources.get_distribution('relstorage')


def _nti_move_from_temp(self, cursor, tid, txn_has_blobs):
    oid_stmt = "SELECT zoid FROM temp_store"

    if self.keep_history:
        stmt = self._move_from_temp_hp_insert_query
        cursor.execute(stmt, (tid,))
    else:
        self._move_from_temp_object_state(cursor, tid)

        if txn_has_blobs:
            # This is where we need to swap out the old
            # relstorage subquery for this double query approach.
            cursor.execute(oid_stmt)
            oids = [oid for (oid,) in fetchmany(cursor)]
            oid_list = ','.join(str(oid) for oid in oids)
            stmt = """
            DELETE FROM blob_chunk
            WHERE zoid IN (%s)
            """
            stmt = stmt % oid_list
            cursor.execute(stmt)

    if txn_has_blobs:
        stmt = self._move_from_temp_copy_blob_query
        cursor.execute(stmt, (tid,))

    cursor.execute(oid_stmt)
    return [oid for (oid,) in fetchmany(cursor)]


def patch():
    if not rel_dist or rel_dist.version <= '2.1a1':
        from relstorage.adapters.mysql.mover import MySQLObjectMover
        MySQLObjectMover.move_from_temp = _nti_move_from_temp
patch()
