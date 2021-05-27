#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from hamcrest import is_
from hamcrest import assert_that

import BTrees
import unittest


class TestPatch(unittest.TestCase):

    def test_patch(self):
        import nti.monkey.patch_btrees_on_import
        assert_that(BTrees.OOBTree.OOBTree.max_internal_size, is_(500))
        assert_that(BTrees.OOBTree.OOBTree.max_leaf_size, is_(120))

        assert_that(BTrees.OOBTree.OOTreeSet.max_internal_size, is_(500))
        assert_that(BTrees.OOBTree.OOTreeSet.max_leaf_size, is_(120))

        assert_that(BTrees.LOBTree.LOBTree.max_internal_size, is_(500))
        assert_that(BTrees.LOBTree.LOBTree.max_leaf_size, is_(240))

        assert_that(BTrees.LOBTree.LOTreeSet.max_internal_size, is_(500))
        assert_that(BTrees.LOBTree.LOTreeSet.max_leaf_size, is_(240))

