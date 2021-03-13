#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python versions prior to 2.7.7 do a very poor job seeding
the random number space. This backport the algorithm from 2.7.7.

.. $Id$
"""

from __future__ import print_function, absolute_import, division

logger = __import__('logging').getLogger(__name__)


from nti.site.site import BTreeLocalAdapterRegistry
BTreeLocalAdapterRegistry.btree_map_threshold = 0

def patch():
    pass
