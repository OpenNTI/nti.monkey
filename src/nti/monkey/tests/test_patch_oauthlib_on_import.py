#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import assert_that
from hamcrest import is_in

import unittest

class TestPatch(unittest.TestCase):

    def test_patch(self):
        from nti.monkey.patch_oauthlib_on_import import patch
        patch()

        from oauthlib.common import urlencoded
        assert_that('\'', is_in(urlencoded))
        assert_that('$', is_in(urlencoded))
        
