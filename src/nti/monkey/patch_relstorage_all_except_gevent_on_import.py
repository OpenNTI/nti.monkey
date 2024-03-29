#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from nti.monkey import patch_pyramid_on_import
from nti.monkey import patch_nti_internal_on_import
from nti.monkey import patch_sqlalchemy_on_import
from nti.monkey import patch_btrees_on_import

logger = __import__('logging').getLogger(__name__)


def patch():
    patch_pyramid_on_import.patch()
    patch_nti_internal_on_import.patch()
    patch_sqlalchemy_on_import.patch()
    patch_btrees_on_import.patch()

patch()
