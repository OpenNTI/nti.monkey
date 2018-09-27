#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Monkey-patch for ZEO to clean up socket no matter what type the
 address is.

 https://github.com/zopefoundation/ZEO/issues/90

.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import six

logger = __import__('logging').getLogger(__name__)


def _nti_clear_socket(self):
    if isinstance(self.options.address, six.string_types):
        try:
            os.unlink(self.options.address)
        except os.error:
            pass


def _patch():
    try:
        from ZEO.runzeo import ZEOServer
        ZEOServer.clear_socket = _nti_clear_socket
    except ImportError:
        pass


_patch()
del _patch


def patch():
    pass
