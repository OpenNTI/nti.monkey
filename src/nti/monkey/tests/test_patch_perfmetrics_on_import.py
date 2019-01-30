#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import assert_that
from hamcrest import has_item

import unittest

from perfmetrics.statsd import StatsdClient
from perfmetrics.statsd import StatsdClientMod
from perfmetrics.statsd import NullStatsdClient

from nti.fakestatsd import FakeStatsDClient
from nti.fakestatsd.matchers import is_set

class TestPatch(unittest.TestCase):

    def test_patch(self):
        from nti.monkey import patch_perfmetrics_on_import

        client = NullStatsdClient()
        client.set_add('metric', 'value')

        client = StatsdClient()
        client.set_add('metric', 'value')

        mod_client = StatsdClientMod(client, 'prefix-%s')
        mod_client.set_add('metric', 'value')

        fake_client = FakeStatsDClient()
        fake_client.set_add('unique', 'chris')
        assert_that(fake_client.metrics, has_item(is_set('unique', 'chris')))
