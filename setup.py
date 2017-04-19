import codecs
from setuptools import setup, find_packages

VERSION = '0.0.0'

entry_points = {
    'console_scripts': [
        "nti_runzeo = nti.monkey.scripts.nti_runzeo:main",
        "nti_zodbconvert = nti.monkey.scripts.nti_zodbconvert:main",
        "nti_multi-zodb-gc = nti.monkey.scripts.nti_multi_zodb_gc:main",
        "nti_multi-zodb-check-refs = nti.monkey.scripts.nti_multi_zodb_check_refs:main",
        # This script overrides the one from ZEO
        "runzeo = nti.monkey.scripts.nti_runzeo:main",
        # This script overrides the one from RelStorage
        "zodbconvert = nti.monkey.scripts.nti_zodbconvert:main",
    ],
}


TESTS_REQUIRE = [
    'nose',
    'nose-timer',
    'nose-pudb',
    'nose-progressive',
    'nose2[coverage_plugin]',
    'pyhamcrest'
]


def _read(fname):
    with codecs.open(fname, encoding='utf-8') as f:
        return f.read()


setup(
    name='nti.monkey',
    version=_read('version.txt').strip(),
    author='Jason Madden',
    author_email='jason@nextthought.com',
    description="NTI Dataserver Monkey Patch",
    long_description=codecs.open('README.rst', encoding='utf-8').read(),
    license='Proprietary',
    keywords='monkey path',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['nti'],
    tests_require=TESTS_REQUIRE,
    install_requires=[
        'setuptools',
        'futures',
        'gevent',
        'nti.transactions',
        'Paste',
        'pymysql',
        'pyramid',
        'python_memcached',
        'RelStorage',
        'repoze.sendmail',
        'repoze.who',
        'six',
        'SQLAlchemy',
        'umysql',
        'umysqldb',
        'WebOb',
        'zc.zodbdgc',
        'ZEO',
        'ZODB',
        'zope.component',
        'zope.dottedname',
        'zope.interface',
        'zope.security',
        'zope.sqlalchemy',
    ],
    extras_require={
        'test': TESTS_REQUIRE,
        ':python_version == "2.7"': [
            # Not ported to Py3 yet; Plus, version 3 adds hard dep on
            # Products.CMFCore/Zope2 that we don't want.
            'plone.i18n < 3.0',
            'zope.browserresource', # Used by plone.i18n implicitly
        ]
    },
    dependency_links=[],
    entry_points=entry_points
)
