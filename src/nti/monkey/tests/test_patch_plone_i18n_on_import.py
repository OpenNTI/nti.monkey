#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import has_entry
from hamcrest import has_length
from hamcrest import assert_that

import unittest


class TestPatch(unittest.TestCase):

    def test_patch(self):
        from nti.monkey.patch_plone_i18n_on_import import _patch
        _patch()

        from plone.i18n.locales.cctld import ccTLDInformation
        assert_that(ccTLDInformation.getAvailableTLDs(), has_length(1400))
        data = ccTLDInformation.getTLDs()
        assert_that(data, has_entry('pub', is_([])))
