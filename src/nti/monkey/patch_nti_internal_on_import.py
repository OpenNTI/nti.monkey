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
    # content search
    moved("nti.contentsearch._content_utils", "nti.contentsearch._deprecated")
    moved("nti.contentsearch._discriminators", "nti.contentsearch._deprecated")
    moved("nti.contentsearch._indexmanager", "nti.contentsearch._deprecated")
    moved("nti.contentsearch._repoze_index", "nti.contentsearch._deprecated")
    moved("nti.contentsearch._whoosh_schemas", "nti.contentsearch._deprecated")
    moved("nti.contentsearch.content_types", "nti.contentsearch._deprecated")
    moved("nti.contentsearch.discriminators", "nti.contentsearch._deprecated")
    moved("nti.contentsearch.indexmanager", "nti.contentsearch._deprecated")
    moved("nti.contentsearch.repoze_adpater", "nti.contentsearch._deprecated")
    moved("nti.contentsearch.whoosh_schemas", "nti.contentsearch._deprecated")
    moved("nti.contentsearch.whoosh_searcher", "nti.contentsearch._deprecated")
    moved("nti.contentsearch.whoosh_storage", "nti.contentsearch._deprecated")
    
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
    moved("nti.utils.property", "nti.property.property")
