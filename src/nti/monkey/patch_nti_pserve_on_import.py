#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)


from nti.monkey import patch_gevent_on_import
patch_gevent_on_import.patch()

from nti.monkey import patch_relstorage_all_on_import
patch_relstorage_all_on_import.patch()

from nti.monkey import patch_random_seed_on_import
patch_random_seed_on_import.patch()

from nti.monkey import patch_pyramid_on_import
patch_pyramid_on_import.patch()


def patch():
    pass
