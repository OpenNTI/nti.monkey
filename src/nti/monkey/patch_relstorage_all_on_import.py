#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Collects all the patches.

.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.monkey import patch_relstorage_query
from nti.monkey import patch_gevent_on_import
from nti.monkey import patch_pyramid_on_import
from nti.monkey import patch_nti_internal_on_import
from nti.monkey import patch_relstorage_umysqldb_on_import

# Order matters
patch_gevent_on_import.patch()
patch_relstorage_umysqldb_on_import.patch()
patch_pyramid_on_import.patch()
patch_nti_internal_on_import.patch()
patch_relstorage_query.patch()


def patch():
    pass
