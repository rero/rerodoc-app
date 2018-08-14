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

from __future__ import absolute_import, print_function

import pkg_resources
from invenio_records_rest.facets import terms_filter
from invenio_search import RecordsSearch
from jsonref import JsonLoader
from jsonresolver.contrib.jsonref import json_loader_factory

from . import facets
from .query import search_factory


# Identity function for string extraction
def _(x):
    return x

# Default language and timezone
BABEL_DEFAULT_LANGUAGE = 'en'
BABEL_DEFAULT_TIMEZONE = 'Europe/Zurich'
I18N_LANGUAGES = [
    ('fr', _('French')),
    ('de', _('German')),
    ('it', _('Italian'))
]

HEADER_TEMPLATE = 'rerodoc_app/header.html'
THEME_HEADER_TEMPLATE = HEADER_TEMPLATE
THEME_FOOTER_TEMPLATE = 'rerodoc_app/footer.html'
BASE_TEMPLATE = 'rerodoc_app/page.html'
COVER_TEMPLATE = 'invenio_theme/page_cover.html'
SETTINGS_TEMPLATE = 'invenio_theme/page_settings.html'
THEME_HEADER_LOGIN_TEMPLATE = 'rerodoc_app/header_login.html'
THEME_LOGO = "img/logo-rero-doc_en.png"

SECRET_KEY = 'default_key'

# Theme
THEME_SITENAME = _('rerodoc-app')

RERODOC_APP_BASE_TEMPLATE = BASE_TEMPLATE
"""Default base template."""
SEARCH_UI_SEARCH_TEMPLATE = "rerodoc_app/search_ui.html"
# SEARCH_UI_HEADER_TEMPLATE = "rerodoc_app/search_header.html"
SEARCH_UI_JSTEMPLATE_COUNT = 'templates/rerodoc_app/count.html'
SEARCH_UI_JSTEMPLATE_FACETS = 'templates/rerodoc_app/facets.html'
SEARCH_UI_JSTEMPLATE_RANGE = \
    'node_modules/invenio-search-js/dist/templates/range.html'
SEARCH_UI_JSTEMPLATE_RESULTS = \
    'templates/rerodoc_app/briefview.html'

JSONSCHEMAS_ENDPOINT = '/schema'
JSONSCHEMAS_HOST = 'rerodoc.test.rero.ch'
JSONSCHEMAS_REGISTER_ENDPOINTS_UI = True


RERODOC_RECORDS_EXPORTFORMATS = {
    'xm': dict(
        title='MARC21 XML',
        serializer='rerodoc_app.records.serializers.marcxml_v1',
        order=2,
    ),
    'json': dict(
        title='JSON',
        serializer='invenio_records_rest.serializers.json_v1',
        order=1,
    ),
    'ld': dict(
        title='JSON-LD',
        serializer='rerodoc_app.records.serializers.ld_json_v1',
        order=3,
    ),
    'turtle': dict(
        title='Turtle',
        serializer='rerodoc_app.records.serializers.ld_turtle_v1',
        order=4,
    ),
    'rdf': dict(
        title='RDF',
        serializer='rerodoc_app.records.serializers.ld_xml_v1',
        order=5,
    ),
    # Unsupported formats.
    'xe': None,
    'xn': None,
    'xw': None,
}

RECORDS_UI_ENDPOINTS = dict(
    recid=dict(
        pid_type='recid',
        route='/record/<pid_value>',
        template='rerodoc_app/record_detail.html'
    ),
    recid_export=dict(
        pid_type='recid',
        route='/record/<pid_value>/export/<any({0}):format>'.format(", ".join(
            list(RERODOC_RECORDS_EXPORTFORMATS.keys()))),
        template='rerodoc_app/record_export.html',
        record_class='invenio_records_files.api:Record',
        view_imp='rerodoc_app.views.records_ui_export'
    ),
    recid_files=dict(
        pid_type='recid',
        route='/record/<pid_value>/files/<path:filename>',
        view_imp='invenio_records_files.utils:file_download_ui',
        record_class='invenio_records_files.api:Record',
    )
)

FILES_REST_PERMISSION_FACTORY = \
    'rerodoc_app.records.permissions:files_permission_factory'

BASE_RECID_REST_ENDPOINTS = dict(
        pid_type='recid',
        pid_minter='rero_recid',
        pid_fetcher='rero_recid',
        # search_type=['record-v1.0.0'],
        search_class=RecordsSearch,
        search_factory_imp=search_factory,
        record_serializers={
            'application/json': ('invenio_records_rest.serializers'
                                 ':json_v1_response'),
            'application/ld+json': ('rerodoc_app.records.serializers'
                                    ':ld_json_v1_response'),
            'text/turtle': ('rerodoc_app.records.serializers'
                            ':ld_turtle_v1_response'),
            'application/rdf+xml': ('rerodoc_app.records.serializers'
                                    ':ld_xml_v1_response'),
            'application/xml': ('rerodoc_app.records.serializers'
                                ':marcxml_v1_response')
        },
        search_serializers={
            'application/json': (
                'rerodoc_app.records.serializers.json_serializer'
                ':json_v1_search'),
            # 'application/ld+json': ('rerodoc.records.serializers'
            #                      ':ld_json_v1_search'),
            # 'text/turtle': ('rerodoc.records.serializers'
            #                      ':ld_turtle_v1_search'),
            # 'application/rdf+xml': ('rerodoc.records.serializers'
            #                      ':ld_xml_v1_search'),
            # 'application/xml': ('rerodoc.records.serializers'
            #                      ':marcxml_v1_search'),
        },
        default_media_type='application/json',
        max_result_window=10000,
     )

RECORDS_REST_ENDPOINTS = dict(
    recid=dict(dict(
        search_index='records',
        list_route='/record/',
        item_route='/record/<pid(recid):pid_value>',
        ), **BASE_RECID_REST_ENDPOINTS),
    iheid=dict(dict(
        search_index='iheid',
        list_route='/iheid/',
        item_route='/iheid/<pid(recid):pid_value>',
        ), **BASE_RECID_REST_ENDPOINTS)
)
RECORDS_REST_FACETS = dict(
    records=dict(
        aggs=dict(
            type=facets.document_type,
            udc=facets.udc,
            institution=facets.institution,
            language=dict(terms=dict(field='language')),
            contributor=dict(terms=dict(field="facet_contributor")),
            keyword=dict(terms=dict(field="facet_keyword"))
        ),
        filters=dict(
            institution=terms_filter('_collections'),
            geneve=terms_filter('_collections'),
            vaud=terms_filter('_collections'),
            fribourg=terms_filter('_collections'),
            neuchatel_jura=terms_filter('_collections'),
            valais=terms_filter('_collections'),

            type=terms_filter('_collections'),
            book=terms_filter('_collections'),

            udc=terms_filter('_collections'),
            sciences_exactes_et_naturelles=terms_filter('_collections'),
            sciences_de_la_terre=terms_filter('_collections'),
            geologie=terms_filter('_collections'),
            contributor=terms_filter('facet_contributor'),
            keyword=terms_filter('facet_keyword'),
            language=terms_filter('language')
        ),
    ),
    iheid=dict(
        aggs=dict(
            # specific collection
            language=dict(
                terms=dict(field="language"),
            ),
            contributor=dict(
                terms=dict(field="facet_contributor"),

            ),
            keyword=dict(
                terms=dict(field="facet_keyword"),
            )
        ),
        filters=dict(
            language=terms_filter('language'),
            contributor=terms_filter('facet_contributor'),
            keyword=terms_filter('facet_keyword'),
            geneve=terms_filter('_collections')
        )
    )
)
# RECORDS_REST_FACETS['records']['aggs'].update(facet_institutions)

RECORDS_REST_SORT_OPTIONS = dict(
    records=dict(
        bestmatch=dict(
            fields=['-_score'],
            title='Best match',
            default_order='asc',
            order=1,
            )
        # ),
        # title=dict(
        #     fields=['title.main.keyword', ],
        #     title='Title',
        #     order=2,
        # )
    )
)

RECORDS_REST_DEFAULT_SORT = dict(
    records=dict(query='bestmatch', noquery='title')
)

SEARCH_UI_SEARCH_API = '/api/record/'

OAISERVER_ID_PREFIX = 'oai:rerodoc:recid'

RERODOC_APP_OAI_JSONSCHEMA = 'records/book-v0.0.1.json'

OAISERVER_CONTROL_NUMBER_FETCHER = 'rero_recid'
OAISERVER_METADATA_FORMATS = {
    'oai_dc': {
        'serializer': (
            'rerodoc.records.serializers.oai.dublin_core', {}
        ),
        'schema': 'http://www.openarchives.org/OAI/2.0/oai_dc.xsd',
        'namespace': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
    },
    'marcxml': {
        'serializer': (
            'invenio_oaiserver.utils:dumps_etree', {
                'prefix': 'book2marc',
            }
        ),
        'schema': 'http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd',
        'namespace': 'http://www.loc.gov/MARC21/slim',
    }
}

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://rerodoc:rerodoc@localhost:5432/rerodoc'  # nopep8
APP_ENABLE_SECURE_HEADERS = 0
INVENIO_DB_VERSIONING = 0


def get_file(url):
    import re
    from invenio_pidstore.resolver import Resolver
    from invenio_records_files.api import Record
    pid, filename = re.search(r'doc.rero.ch/record/(\w+)/files/(.*)', url).groups()
    resolver = Resolver('recid', 'rec', Record.get_record)
    pid, record = resolver.resolve(pid)
    return record.files[filename].obj.file.storage().fileurl.replace('file://', '')


MULTIVIO_FILENAME_TO_PATH = get_file
