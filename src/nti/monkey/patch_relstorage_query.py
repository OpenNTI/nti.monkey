#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Monkey-patch for RelStorage to not use subqueries. Our older mysql version
    (5.5.*) ends up not using the index and does a full-table scan. This should
    be improved/fixed in mysql 5.6.5.

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from relstorage.iter import fetchmany


def _nti_move_from_temp_object_state(self, cursor, tid):
    """
    Called for history-free databases.
    Should replace all entries in object_state with the
    same zoid from temp_store.
    """
    oid_stmt = """
    SELECT zoid FROM temp_store
    """
    cursor.execute(oid_stmt)
    oids = [oid for (oid,) in fetchmany(cursor)]
    oids = ','.join(str(oid) for oid in oids)

    stmt = """
     DELETE FROM object_state
     WHERE zoid IN (%s)
     """
    stmt = stmt % oids
    cursor.execute(stmt)

    stmt = self._move_from_temp_hf_insert_query
    cursor.execute(stmt, (tid,))


def _nti_move_from_temp(self, cursor, tid, txn_has_blobs):
    """
    Moved the temporarily stored objects to permanent storage.
    Returns the list of oids stored.
    """
    oid_stmt = """
    SELECT zoid FROM temp_store
    """

    if self.keep_history:
        stmt = self._move_from_temp_hp_insert_query
        cursor.execute(stmt, (tid,))
    else:
        _nti_move_from_temp_object_state(self, cursor, tid)

        if txn_has_blobs:
            cursor.execute(oid_stmt)
            oids = [oid for (oid,) in fetchmany(cursor)]
            oid_list = ','.join(str(oid) for oid in oids)
            stmt = """
        	DELETE FROM blob_chunk
        	WHERE zoid IN (%s)
        	"""
            cursor.execute(stmt, (oid_list,))

    if txn_has_blobs:
        stmt = self._move_from_temp_copy_blob_query
        cursor.execute(stmt, (tid,))

    cursor.execute(oid_stmt)
    return [oid for (oid,) in fetchmany(cursor)]


def patch():
    from relstorage.adapters.mover import AbstractObjectMover
    AbstractObjectMover.move_from_temp = _nti_move_from_temp
    AbstractObjectMover._move_from_temp_object_state = _nti_move_from_temp_object_state

patch()
