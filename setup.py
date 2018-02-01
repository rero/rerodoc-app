# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017 RERO.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, RERO does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""RERO DOC Invenio application."""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

tests_require = [
    'check-manifest>=0.25',
    'coverage>=4.0',
    'isort>=4.2.2',
    'pydocstyle>=1.0.0',
    'pytest-cache>=1.0',
    'pytest-cov>=1.8.0',
    'pytest-pep8>=1.0.6',
    'pytest>=2.8.0',
]

extras_require = {
    'docs': [
        'Sphinx>=1.5.1',
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for reqs in extras_require.values():
    extras_require['all'].extend(reqs)

setup_requires = [
    'Babel>=1.3',
    'pytest-runner>=2.6.2',
]

install_requires = [
    'Flask-BabelEx>=0.9.2',
    'Flask-CLI>=0.4.0',
    'Flask-CORS>=2.1.0',
    'invenio-app>=1.0.0b1',
    'invenio-assets>=1.0.0b7',
    'invenio-base>=1.0.0a16',
    'invenio-cache>=1.0.0b1',
    'invenio-config>=1.0.0b3',
    'invenio-db[postgresql]>=1.0.0b9',
    'invenio-i18n>=1.0.0b4',
    'invenio-indexer>=1.0.0a10',
    'invenio-jsonschemas>=1.0.0a7',
    'invenio-marc21>=1.0.0a5',
    'invenio-oaiserver>=1.0.0a14',
    'invenio-pidstore>=1.0.0b2',
    'invenio-query-parser>=0.6.0',
    'invenio-records>=1.0.0b4',
    'invenio-records-rest>=1.0.0b3',
    'invenio-records-ui>=1.0.0b1',
    'invenio-files-rest>=1.0.0a22',
    'invenio-records-files>=1.0.0a10',
    'invenio-rest>=1.0.0b2',
    'invenio-search[elasticsearch5]>=1.0.0b1',
    'invenio-search-ui>=1.0.0a9',
    'invenio-theme>=1.0.0b4',
    'invenio-access>=1.0.0b1',
    'invenio-accounts>=1.0.0b10',
    'invenio-admin>=1.0.0b4',
    'invenio-celery>=1.0.0b3',
    'invenio-oaiharvester>=1.0.0a3',
    #'invenio-collections>=1.0.0a4',
    'PyPDF2 >=1.26.0',
    'PyLD>=0.8.2',
    'slate3k>=0.5.3',
    'Markdown>=2.6.10',
    'rdflib>=4.2.2',
    'rdflib-jsonld>=0.4.0',
    'Wand>=0.4.4',
    'isbnlib>=3.8.3'
]

packages = find_packages()


# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('rerodoc_app', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='rerodoc-app',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='invenio TODO',
    license='GPLv2',
    author='RERO',
    author_email='software@rero.ch',
    url='https://github.com/rero/rerodoc-app',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'flask.commands': [
            'utils = rerodoc_app.cli:utils',
        ],
        'invenio_base.apps': [
            'rerodoc_app = rerodoc_app:RerodocApp',
        ],
        'invenio_i18n.translations': [
            'messages = rerodoc_app',
        ],
        'invenio_config.module': [
            'rerodoc_app = rerodoc_app.config',
        ],
        'invenio_assets.bundles': [
            'rerodoc_search_js = rerodoc_app.bundles:search_js',
            'rerodoc_css = rerodoc_app.bundles:css',
            'rerodoc_frontpage_css = rerodoc_app.bundles:frontpage_css'
        ],
        'dojson.cli.rule': [
            'book = rerodoc_app.records.dojson:book',
            'book2marc = rerodoc_app.records.dojson:book2marc',
            'audio = rerodoc_app.records.dojson:audio',
            'book2audio = rerodoc_app.records.dojson:audio2marc'
        ],
        'invenio_pidstore.minters': [
            'rero_recid = rerodoc_app.records.minters:recid_minter'
        ],
        'invenio_pidstore.fetchers': [
            'rero_recid = rerodoc_app.records.fetchers:recid_fetcher'
        ],
        'invenio_jsonschemas.schemas': [
            'record = rerodoc_app.records.jsonschemas'
        ],
        'invenio_search.mappings': [
            'records = rerodoc_app.records.mappings'
        ],
        'invenio_celery.tasks': [
            'rerodoc_app = rerodoc_app.records.tasks',
        ],
        # TODO: Edit these entry points to fit your needs.
        # 'invenio_access.actions': [],
        # 'invenio_admin.actions': [],
        # 'invenio_assets.bundles': [],
        # 'invenio_base.api_apps': [],
        # 'invenio_base.api_blueprints': [],
        # 'invenio_base.blueprints': [],
        # 'invenio_celery.tasks': [],
        # 'invenio_db.models': [],
        # 'invenio_pidstore.minters': [],
        # 'invenio_records.jsonresolver': [],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 1 - Planning',
    ],
)
