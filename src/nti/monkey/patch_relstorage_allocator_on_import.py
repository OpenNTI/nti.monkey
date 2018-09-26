#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Add some audit logging to cursor error conditions seen in prod.

.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

logger = __import__('logging').getLogger(__name__)


def _patch_allocator_logging(cls):
    """
    Patch allocation logging. We copied the actual `new_oids` func, while
    handling for `n == 0` and logging.
    """

    def new_oids(self, cursor):
        """Return a sequence of new, unused OIDs."""
        stmt = "INSERT INTO new_oid VALUES ()"
        cursor.execute(stmt)
        # This is a DB-API extension. Fortunately, all
        # supported drivers implement it. (In the past we used
        # cursor.connection.insert_id(), which was specific to MySQLdb)
        n = cursor.lastrowid

        # At least in one setup (gevent/umysqldb/pymysql/mysql 5.5)
        # we have observed cursor.lastrowid to be None
        # - and also presumably zero.
        if n is None or n == 0:
            # pylint:disable=protected-access
            logger.warn('Invalid lastrowid when generating new zoids (%s) (%s)',
                        n, getattr(cursor, '_executed', None))
            raise self.disconnected_exception("Invalid return for lastrowid")

        if n % 1000 == 0:
            # Clean out previously generated OIDs.
            stmt = "DELETE FROM new_oid WHERE zoid < %s"
            cursor.execute(stmt, (n,))
        return self._oid_range_around(n)
    cls.new_oids = new_oids

def _patch():
    from relstorage.adapters.mysql import oidallocator
    # The various lockers may be directly imported in random places
    # already, so we need to patch in place
    _patch_allocator_logging(oidallocator.MySQLOIDAllocator)

_patch()
del _patch

def patch():
    pass
