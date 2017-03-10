#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This package contains modules that monkey-patch various parts of the system. Typically they
will do so on import (specified in the name) but will also provide a 'patch' function to avoid
"unused import" warnings. Each module will have minimal dependencies so it can be imported as 
early as possible.

.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.monkey.patches import patch_repoze_sendmail
from nti.monkey.patches import patch_gevent_on_import
from nti.monkey.patches import patch_pyramid_on_import
from nti.monkey.patches import patch_random_seed_on_import
from nti.monkey.patches import patch_nti_internal_on_import
from nti.monkey.patches import patch_relstorage_all_on_import
from nti.monkey.patches import patch_relstorage_umysqldb_on_import
from nti.monkey.patches import patch_paste_auth_tkt_sha512_on_import
from nti.monkey.patches import patch_webob_cookie_escaping_on_import
from nti.monkey.patches import patch_relstorage_all_except_gevent_on_import

from nti.monkey.scripts import nti_runzeo
from nti.monkey.scripts import nti_zodbconvert
from nti.monkey.scripts import nti_multi_zodb_gc
from nti.monkey.scripts import nti_multi_zodb_check_refs
