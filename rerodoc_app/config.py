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


# Identity function for string extraction
def _(x):
    return x

# Default language and timezone
BABEL_DEFAULT_LANGUAGE = 'en'
BABEL_DEFAULT_TIMEZONE = 'Europe/Zurich'
I18N_LANGUAGES = [
]

HEADER_TEMPLATE = 'invenio_theme/header.html'
BASE_TEMPLATE = 'invenio_theme/page.html'
COVER_TEMPLATE = 'invenio_theme/page_cover.html'
SETTINGS_TEMPLATE = 'invenio_theme/page_settings.html'

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

RECORDS_REST_ENDPOINTS = dict(
    recid=dict(
        pid_type='recid',
        pid_minter='rero_recid',
        pid_fetcher='rero_recid',
        search_index='records',
        search_type=None,
        record_serializers={
            'application/json': ('invenio_records_rest.serializers'
                                 ':json_v1_response'),
        },
        search_serializers={
            'application/json': ('invenio_records_rest.serializers'
                                 ':json_v1_search'),
        },
        list_route='/records/',
        item_route='/records/<pid(recid):pid_value>',
        default_media_type='application/json',
        max_result_window=10000,
    )
)
OAIHARVESTER_WORKDIR='/Users/maj/devel/virtualenvs/rerodoc-app/var/instance'
from jsonresolver import JSONResolver

from jsonresolver.contrib.jsonref import json_loader_factory
JSONSCHEMAS_LOADER_CLS = json_loader_factory(JSONResolver(
    plugins=['invenio_jsonschemas.jsonresolver']
))
