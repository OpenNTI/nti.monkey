#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from nti.monkey.deprecated import moved

def patch():    
    # deprecated core/fragments pkgs
    moved("nti.dataserver.core", "nti.coremetadata")
    moved("nti.dataserver.core.interfaces", "nti.coremetadata.interfaces")
    moved("nti.dataserver_core", "nti.coremetadata")
    moved("nti.dataserver_core.mixins", "nti.coremetadata.mixins")
    moved("nti.dataserver_core.schema", "nti.coremetadata.schema")
    moved("nti.dataserver_core.interfaces", "nti.coremetadata.interfaces")
    
    moved("nti.dataserver.fragments", "nti.coremetadata")
    moved("nti.dataserver.fragments.interfaces", "nti.coremetadata.interfaces")
    moved("nti.dataserver_fragments", "nti.coremetadata")
    moved("nti.dataserver_fragments.mixins", "nti.coremetadata.mixins")
    moved("nti.dataserver_fragments.schema", "nti.coremetadata.schema")
    moved("nti.dataserver_fragments.interfaces", "nti.coremetadata.interfaces")

    # metadata index 
    moved("nti.dataserver.metadata_index", "nti.dataserver.metadata.index")

    # deleted session_consumer module
    moved("nti.dataserver.session_consumer", "nti.socketio.session_consumer")

    # utils
    moved("nti.utils.interfaces", "nti.common.interfaces")
    moved("nti.utils.ldap", "nti.common.model")
    moved("nti.utils.oauthkeys", "nti.common.model")
    moved("nti.utils.property", "nti.property.property")
