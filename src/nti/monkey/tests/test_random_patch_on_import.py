#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

import unittest

from hamcrest import is_
from hamcrest import assert_that

class TestPatch(unittest.TestCase):

	def test_patch(self):
		from ..random_seed_patch_on_import import _do_patch
		_do_patch()

		import random
		assert_that( random.seed.__module__,
					 is_('nti.monkey.random_seed_patch_on_import'))

		random.seed()
