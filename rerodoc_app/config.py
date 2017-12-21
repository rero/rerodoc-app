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
from jsonresolver import JSONResolver
from jsonresolver.contrib.jsonref import json_loader_factory

from invenio_records_rest.facets import terms_filter
from invenio_search import RecordsSearch

from .facets import facet_document_type, facet_institutions
from .query import search_factory


# Identity function for string extraction
def _(x):
    return x

# Default language and timezone
BABEL_DEFAULT_LANGUAGE = 'fr'
BABEL_DEFAULT_TIMEZONE = 'Europe/Zurich'
I18N_LANGUAGES = [
    ('fr', _('French')),
    ('de', _('German')),
    ('it', _('Italian'))
]

HEADER_TEMPLATE = 'invenio_theme/header.html'
BASE_TEMPLATE = 'invenio_theme/page.html'
COVER_TEMPLATE = 'invenio_theme/page_cover.html'
SETTINGS_TEMPLATE = 'invenio_theme/page_settings.html'
THEME_LOGO = "img/logo-rero-doc_en.png"

SECRET_KEY = 'default_key'

# Theme
THEME_SITENAME = _('rerodoc-app')

RERODOC_APP_DEFAULT_VALUE = 'foobar'
"""Default value for the application."""

RERODOC_APP_BASE_TEMPLATE = BASE_TEMPLATE
"""Default base template."""

SEARCH_UI_JSTEMPLATE_RESULTS = \
    'templates/rerodoc_data/briefview.html'

JSONSCHEMAS_ENDPOINT = '/schema'
JSONSCHEMAS_HOST = 'rerodoc.test.rero.ch'
JSONSCHEMAS_REGISTER_ENDPOINTS_UI = True
JSONSCHEMAS_REGISTER_ENDPOINTS_API = True
JSONSCHEMAS_REPLACE_REFS = False
JSONSCHEMAS_RESOLVE_SCHEMA = False

RERODOC_RECORDS_EXPORTFORMATS = {
    'xm': dict(
        title='MARC21 XML',
        serializer='rerodoc_data.serializers.marcxml_v1',
        order=2,
    ),
    'json': dict(
        title='JSON',
        serializer='invenio_records_rest.serializers.json_v1',
        order=1,
    ),
    'ld': dict(
        title='JSON-LD',
        serializer='rerodoc_data.serializers.ld_json_v1',
        order=3,
    ),
    'turtle': dict(
        title='Turtle',
        serializer='rerodoc_data.serializers.ld_turtle_v1',
        order=4,
    ),
    'rdf': dict(
        title='RDF',
        serializer='rerodoc_data.serializers.ld_xml_v1',
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
        template='rerodoc/record_detail.html'
    ),
    recid_export=dict(
        pid_type='recid',
        route='/record/<pid_value>/export/<any({0}):format>'.format(", ".join(
            list(RERODOC_RECORDS_EXPORTFORMATS.keys()))),
        template='rerodoc/record_export.html',
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
    'rerodoc_data.permissions:files_permission_factory'

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
            'application/ld+json': ('rerodoc_data.serializers'
                                    ':ld_json_v1_response'),
            'text/turtle': ('rerodoc_data.serializers'
                            ':ld_turtle_v1_response'),
            'application/rdf+xml': ('rerodoc_data.serializers'
                                    ':ld_xml_v1_response'),
            'application/xml': ('rerodoc_data.serializers'
                                ':marcxml_v1_response')
        },
        search_serializers={
            'application/json': ('rerodoc_data.serializers.json_serializer'
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
            doc_type=facet_document_type,
            intitutions=facet_institutions,
            language=dict(
                terms=dict(field="language"),
            ),
            authors=dict(
                terms=dict(field="facet_author"),

            ),
            # UDC
            keywords=dict(
                terms=dict(field="facet_keyword"),
            )
        ),
        filters=dict(
            institutions=terms_filter('_collections'),
            geneve=terms_filter('_collections'),
            vaud=terms_filter('_collections'),
            fribourg=terms_filter('_collections'),
            neuchatel=terms_filter('_collections'),
            language=terms_filter('language'),
            doc_type=terms_filter('_collections'),
            book=terms_filter('_collections'),
            authors=terms_filter('facet_author'),
            keywords=terms_filter('facet_keyword')
        ),
    ),
    iheid=dict(
        aggs=dict(
            # specific collection
            language=dict(
                terms=dict(field="language"),
            ),
            authors=dict(
                terms=dict(field="facet_author"),

            ),
            # UDC
            keywords=dict(
                terms=dict(field="facet_keyword"),
            )
        ),
        filters=dict(
            geneve=terms_filter('_collections'),
            language=terms_filter('language'),
            authors=terms_filter('facet_author'),
            keywords=terms_filter('facet_keyword')
        )
    )
)

RECORDS_REST_SORT_OPTIONS = dict(
    records=dict(
        bestmatch=dict(
            fields=['-_score'],
            title='Best match',
            default_order='asc',
            order=1,
        ),
        title=dict(
            fields=['title.full', ],
            title='Title',
            order=2,
        )
    )
)

RECORDS_REST_DEFAULT_SORT = dict(
    records=dict(query='bestmatch', noquery='title')
)

SEARCH_UI_SEARCH_API = '/api/record/'

OAISERVER_ID_PREFIX = 'oai:rerodoc:recid'

SEARCH_UI_JSTEMPLATE_RESULTS = \
    'templates/rerodoc/record_brief.html'
SEARCH_UI_SEARCH_TEMPLATE = "rerodoc/search_ui.html"
SEARCH_UI_JSTEMPLATE_FACETS = 'templates/rerodoc/facets.html'
SEARCH_UI_JSTEMPLATE_RANGE = \
    'node_modules/invenio-search-js/dist/templates/range.html'

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


JSONSCHEMAS_LOADER_CLS = json_loader_factory(JSONResolver(
    plugins=['invenio_jsonschemas.jsonresolver']
))
