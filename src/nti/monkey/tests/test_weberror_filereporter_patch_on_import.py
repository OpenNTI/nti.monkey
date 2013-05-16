#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""


$Id$
"""

from __future__ import print_function, unicode_literals, absolute_import
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

#disable: accessing protected members, too many methods
#pylint: disable=W0212,R0904


from hamcrest import assert_that
from hamcrest import is_
from hamcrest import has_key
from hamcrest import has_property

import nti.tests

def test_patch():
	import nti.monkey.weberror_filereporter_patch_on_import
	nti.monkey.weberror_filereporter_patch_on_import.patch()

	assert_that( nti.monkey.weberror_filereporter_patch_on_import, has_property( 'patched', True ) )