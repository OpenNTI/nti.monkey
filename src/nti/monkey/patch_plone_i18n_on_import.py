#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

resource_filename = __import__('pkg_resources').resource_filename


def _patch():
    try:
        import csv
        from plone.i18n.locales import cctld
        _tld_to_language = cctld._tld_to_language

        holder = []
        source = resource_filename(__name__, 'resources/iana.csv')
        with open(source, 'rU') as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                if row:
                    domain = row[0][1:]  # remove dot
                    if domain not in _tld_to_language:
                        _tld_to_language[domain] = holder
    except ImportError:
        import warnings
        warnings.warn("plone.i18n is not available")


def patch():
    pass
_patch()
