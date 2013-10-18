#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""


$Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

#disable: accessing protected members, too many methods
#pylint: disable=W0212,R0904


from hamcrest import assert_that
from hamcrest import is_
from hamcrest import has_key
from hamcrest import has_property

from nti.testing import base
from nti.testing.matchers import validly_provides

import plone.namedfile.interfaces as nfile_interfaces
import zope.file.interfaces as zfile_interfaces

import zope.file.file as zfile
import plone.namedfile.file as nfile

from .. import plonefile_zopefile_patch_on_import

# so that storages work, plone.namedfile reg must be set up
setUpModule = lambda: base.module_setup( set_up_packages=('nti.dataserver.contenttypes',) )
tearDownModule = base.module_teardown

def test_patch():
	plonefile_zopefile_patch_on_import.patch()

	nf = nfile.NamedFile(data='data', contentType=b'text/plain', filename='foo.txt')
	nbf = nfile.NamedBlobFile(data='data', contentType=b'text/plain', filename='foo.txt')
	nif = nfile.NamedBlobFile(data='data', contentType=b'image/gif', filename='foo.txt')
	for f in nf, nbf, nif:
		assert_that( f,
					 validly_provides(nfile_interfaces.IFile ) )
		assert_that( f, has_property( '__name__', 'foo.txt' ) )


	# Check that we sniff the data using zope.mimetype.
	nf = nfile.NamedFile( data="<?xml?><config />" )
	nf.mimeType = nfile.get_contenttype( file=nf )
	assert_that( nf,
				 has_property( 'contentType', 'text/xml' ) )
