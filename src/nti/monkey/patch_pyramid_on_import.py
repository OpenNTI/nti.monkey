#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import pkg_resources

pyramid_dist = pkg_resources.get_distribution('pyramid')
zcml_dist = pkg_resources.get_distribution('pyramid-zcml')

if      pyramid_dist.version and pyramid_dist.version >= '1.8' \
    and zcml_dist.version and zcml_dist.version <= '1.0':

    import pyramid.config
    from pyramid.config import Configurator
    from pyramid.asset import resolve_asset_spec

    class _Configurator(Configurator):

        def _split_spec(self, path_or_spec):
            return resolve_asset_spec(path_or_spec, self.package_name)

    pyramid.config.Configurator = _Configurator


def patch():
    pass
