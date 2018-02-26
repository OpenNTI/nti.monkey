#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Collects all the patches.

.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from nti.monkey import patch_gevent_on_import
from nti.monkey import patch_pyramid_on_import
from nti.monkey import patch_nti_internal_on_import
from nti.monkey import patch_relstorage_locker_on_import
from nti.monkey import patch_relstorage_umysqldb_on_import

logger = __import__('logging').getLogger(__name__)

# Order matters
patch_gevent_on_import.patch()
patch_relstorage_umysqldb_on_import.patch()
patch_pyramid_on_import.patch()
patch_nti_internal_on_import.patch()
patch_relstorage_locker_on_import.patch()


def patch():
    pass
