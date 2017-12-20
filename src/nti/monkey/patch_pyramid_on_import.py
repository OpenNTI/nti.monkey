#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import pkg_resources

pyramid_dist = pkg_resources.get_distribution('pyramid')
zcml_dist = pkg_resources.get_distribution('pyramid-zcml')

logger = __import__('logging').getLogger(__name__)

if      pyramid_dist.version and pyramid_dist.version >= '1.8' \
    and zcml_dist.version and zcml_dist.version <= '1.0':

    import pyramid.config
    from pyramid.asset import resolve_asset_spec

    class _Configurator(pyramid.config.Configurator):

        def _split_spec(self, path_or_spec):
            return resolve_asset_spec(path_or_spec, self.package_name)

    pyramid.config.Configurator = _Configurator


def patch():
    pass
