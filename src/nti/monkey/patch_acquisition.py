#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import sys
import types

from zope import interface

try:
    from Acquisition.interfaces import IAcquirer
except ImportError:
    class IAcquirer(interface.Interface):
        pass

try:
    from Acquisition import Implicit
except ImportError:
    @interface.implementer(IAcquirer)
    class Implicit(object):
        pass

try:
    from ExtensionClass import Base
except ImportError:
    class Base(object):
        pass
Base = Base  # pylint

try:
    from Acquisition import aq_base
except ImportError:
    def aq_base(o):
        return o


def patch():
    if 'Acquisition' not in sys.modules:
        Acquisition = types.ModuleType(str("Acquisition"))
        Acquisition.Implicit = Implicit
        Acquisition.aq_base = aq_base
        sys.modules[Acquisition.__name__] = Acquisition
