#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Patch some issues in relstorage's locker module: proved a better
error when commit locking fails, and track the time that a lock is
held (in mysql).

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os
import time

import gc as GC

from relstorage.adapters.interfaces import UnableToAcquireCommitLockError


LONG_LOCK_TIME_IN_SECONDS = 1

def _patch_hold_logging(cls):

    cls.locked_at = 0
    cls.original_gc_count = None

    orig_hold = cls.hold_commit_lock
    orig_release = cls.release_commit_lock

    # depending on the 'nowait' argument, locking
    # will either return a boolean (if true)
    # or raise a storage error (if locking failed) or None (if locking worked)
    # There can be priority inversions here because this lock
    # is totally out of gevent/threadings control; it would almost
    # be nice to raise our priority or even stop task switching
    # altogether while we hold this.
    def hold_commit_lock(self, *args, **kwargs):
        try:
            result = orig_hold(self, *args, **kwargs)
        except UnableToAcquireCommitLockError:
            self.locked_at = 0
            self.original_gc_count = None
            raise
        else:
            self.locked_at = time.time() if result is None or result else 0
            self.original_gc_count = GC.get_count()
            return result

    def release_commit_lock(self, cursor):
        now = time.time()
        try:
            return orig_release(self, cursor)
        except AssertionError:
            logger.warn('Cursor error when releasing lock (%s)',
                        getattr(cursor, '_executed', None))
            raise IOError('Invalid cursor result while releasing lock')
        finally:
            locked_at = self.locked_at
            original_gc_count = self.original_gc_count
            self.locked_at = 0
            self.original_gc_count = None
            self.gc_object_count = None
            if locked_at:
                duration = now - locked_at
                if duration > LONG_LOCK_TIME_IN_SECONDS:
                    lock_release = time.time() - now
                    logger.warn("Held global commit locks for (%.3fs) (release_time=%.3fs) %s (%s) (original_gen_count=%s) (gen_count=%s) (object_count=%s)",
                                duration,
                                lock_release,
                                os.getloadavg(),
                                getattr(getattr(cursor, 'connection', ''), 'db', ''),
                                original_gc_count,
                                GC.get_count(),
                                len(GC.get_objects()))

    cls.hold_commit_lock = hold_commit_lock
    cls.release_commit_lock = release_commit_lock

def _patch():
    from relstorage.adapters.mysql import locker as mysql_locker
    from relstorage.adapters.oracle import locker as oracle_locker
    from relstorage.adapters.postgresql import locker as postgresql_locker
    # The various lockers may be directly imported in random places
    # already, so we need to patch in place
    _patch_hold_logging(mysql_locker.MySQLLocker)
    _patch_hold_logging(oracle_locker.OracleLocker)
    _patch_hold_logging(postgresql_locker.PostgreSQLLocker)

_patch()
del _patch

def patch():
    pass
