#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from hamcrest import not_none
from hamcrest import assert_that
from hamcrest import instance_of

import unittest

from sqlalchemy import create_engine

from nti.monkey.patch_sqlalchemy_on_import import geventMysqlclient_dialect


class TestPatch(unittest.TestCase):

    def test_patch(self):
        from nti.monkey.patch_sqlalchemy_on_import import patch
        patch()
        engine = create_engine('gevent_mysql:///testdb.db')
        assert_that(engine, not_none())
        assert_that(engine.dialect, instance_of(geventMysqlclient_dialect))
