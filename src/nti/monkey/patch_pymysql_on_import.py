#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import pkg_resources

pymysql_dist = pkg_resources.get_distribution('pymysql')

logger = __import__('logging').getLogger(__name__)

if pymysql_dist.version and pymysql_dist.version >= '1.8':

    import pymysql.constants
    import pymysql.connections

    class _Connection(pymysql.connections.Connection):

        def __ini__(self, *args, **kwargs):
            kwargs['binary_prefix'] = True
            client_flag = kwargs.pop('client_flag')
            if client_flag is None:
                client_flag = pymysql.constants.CLIENT.MULTI_STATEMENTS
            else:
                client_flag = client_flag | pymysql.constants.CLIENT.MULTI_STATEMENTS
            kwargs['client_flag'] = client_flag
            super(_Connection, self).__init__(*args, **kwargs)

    pymysql.connections.Connection = _Connection
    pymysql.Connection = _Connection


def patch():
    pass
