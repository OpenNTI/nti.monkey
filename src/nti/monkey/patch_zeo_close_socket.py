#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Monkey-patch for ZEO to clean up socket no matter what type the
    address is.

    https://github.com/zopefoundation/ZEO/issues/90

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import os
import six

def _nti_clear_socket(self):
    if isinstance(self.options.address, six.string_types):
        try:
            os.unlink(self.options.address)
        except os.error:
            pass


def patch():
    try:
        from ZEO.runzeo import ZEOServer
        ZEOServer.clear_socket = _nti_clear_socket
    except ImportError:
        pass
patch()
