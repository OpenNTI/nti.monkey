#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division

logger = __import__('logging').getLogger(__name__)


from nti.site.site import BTreeLocalAdapterRegistry
BTreeLocalAdapterRegistry.btree_map_threshold = 0

def patch():
    pass
