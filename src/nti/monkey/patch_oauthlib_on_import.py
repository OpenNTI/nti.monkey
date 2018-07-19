#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: patch_oauthlib_on_import 125022 2017-12-20 16:35:06Z carlos.sanchez $
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from oauthlib.common import urlencoded

_ALSO_ALLOWED_CHARS = set('$\'')

# Patch for https://github.com/oauthlib/oauthlib/issues/563
# while we wait for a formal fix there
assert _ALSO_ALLOWED_CHARS - urlencoded, 'All chars included. Patch no longer needed?'
urlencoded.update(_ALSO_ALLOWED_CHARS)

def patch():
    pass
