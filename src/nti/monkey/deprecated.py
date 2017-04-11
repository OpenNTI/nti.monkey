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
import warnings
import functools

import zope.deferredimport.deferredmodule

import zope.deprecation


def deprecated(replacement=None):  # annotation factory

    def outer(oldfun):
        im_class = getattr(oldfun, 'im_class', None)
        if im_class:
            n = '%s.%s.%s' % (im_class.__module__,
                              im_class.__name__,
                              oldfun.__name__)
        else:
            n = oldfun.__name__

        msg = "%s is deprecated" % n
        if replacement is not None:
            msg += "; use %s instead" % (replacement.__name__)
        return zope.deprecation.deprecate(msg)(oldfun)
    return outer

zope.deprecation.deprecation.__dict__['DeprecationWarning'] = FutureWarning

# The 'moved' method doesn't pay attention to the 'show' flag, which
# produces annoyances in backwards compatibility and test code. Make it do so.
# The easiest way os to patch the warnings module it uses. Fortunately, it only
# uses one method


class _warnings(object):

    def warn(self, msg, typ, stacklevel=0):
        if zope.deprecation.__show__():
            warnings.warn(msg, typ, stacklevel + 1)

    def __getattr__(self, name):
        # Let everything else flow through to the real module
        return getattr(warnings, name)

zope.deprecation.deprecation.__dict__['warnings'] = _warnings()

# encourage importing from here so we're sure our patch is applied
moved = zope.deprecation.moved

# deferred import has the same problems
zope.deferredimport.deferredmodule.__dict__['warnings'] = _warnings()
zope.deferredimport.deferredmodule.__dict__['DeprecationWarning'] = FutureWarning

# NOTE: There is a substantial problem with zope.deferredimport.deferredmodule/deprecatedFrom
# and the like: it loses access to the module __doc__, which makes Sphinx and the like useless
# For this reason, prefer zope.deprecation.


class hiding_warnings(object):
    """
    A context manager that executes its body in a context
    where deprecation warnings are not shown.
    """

    def __enter__(self):
        zope.deprecation.__show__.off()

    def __exit__(self, *args):
        zope.deprecation.__show__.on()


def hides_warnings(f):
    """
    A decorator that causes the wrapped function to not show warnings when
    it executes.
    """
    @functools.wraps(f)
    def inner(*args, **kwargs):
        with hiding_warnings():
            return f(*args, **kwargs)
    return inner


def moved(from_location, to_location):
    try:
        __import__(from_location)
    except ImportError:
        module = types.ModuleType(str(from_location), "Created module")
        sys.modules[from_location] = module

    message = '%s has moved to %s.' % (from_location, to_location)
    warnings.warn(message, DeprecationWarning, 3)
    try:
        __import__(to_location)
    except ImportError:
        module = types.ModuleType(str(to_location), "Created module")
        sys.modules[to_location] = module

    fromdict = sys.modules[to_location].__dict__
    to_mod = sys.modules[from_location]
    to_mod.__doc__ = message

    for name, v in fromdict.items():
        if name not in to_mod.__dict__:
            setattr(to_mod, name, v)
    return to_mod
