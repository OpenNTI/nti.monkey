#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Perfmetrics versions up to and including 2.0.0 do not provide a public
convenience function for sending statsd set metrics. This monkey patches
that in to the 3 perfmetrics implemented clients.
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

def _patch():
    try:
        from perfmetrics.statsd import StatsdClient, StatsdClientMod, NullStatsdClient
    except ImportError:
        return

    for clazz in (StatsdClient, StatsdClientMod, NullStatsdClient):
        if hasattr(clazz, 'set_add'):
            logger.warn('Not patching set_add into perfmetrics')
            return

    def _set_add(self, stat, value):
        self._send('%s:%s|s' % (stat, value))
    StatsdClient.set_add = _set_add

    def _set_add(self, stat, *args, **kw):
        self._wrapped.set_add(self.format % stat, *args, **kw)
    StatsdClientMod.set_add = _set_add

    def _set_add(self, stat, *args, **kw):
        pass
    NullStatsdClient.set_add = _set_add


_patch()
del _patch

def patch():
    pass
