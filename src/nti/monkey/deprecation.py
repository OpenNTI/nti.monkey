#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import sys
import types
import warnings

logger = __import__('logging').getLogger(__name__)


def moved(from_location, to_location):
    try:
        __import__(to_location)
    except ImportError:
        message = '%s cannot be found.' % to_location
        warnings.warn(message, DeprecationWarning, 3)
        return

    try:
        __import__(from_location)
    except ImportError:
        module = types.ModuleType(str(from_location), "Created module")
        sys.modules[from_location] = module

    message = '%s has moved to %s.' % (from_location, to_location)
    warnings.warn(message, DeprecationWarning, 3)

    fromdict = sys.modules[to_location].__dict__
    to_mod = sys.modules[from_location]
    to_mod.__doc__ = message

    for name, v in fromdict.items():
        if name not in to_mod.__dict__:
            setattr(to_mod, name, v)
    return to_mod
