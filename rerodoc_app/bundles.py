# -*- coding: utf-8 -*-
#
# This file is part of Zenodo.
# Copyright (C) 2015, 2016 CERN.
#
# Zenodo is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Zenodo is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Zenodo; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""JS/CSS bundles for theme."""

from __future__ import absolute_import, print_function

import os

from flask_assets import Bundle
from pkg_resources import resource_filename

from invenio_assets import AngularGettextFilter, GlobBundle, NpmBundle, \
    current_assets
from invenio_theme.bundles import js as base_js

css = NpmBundle(
    'scss/styles.scss',
    depends=('scss/*.scss', ),
    filters='node-scss, cleancssurl',
    output='gen/rerodoc.%(version)s.css',
    npm={
        "almond": "~0.3.1",
        "bootstrap-sass": "~3.3.5",
        "font-awesome": "~4.4.0"
    }
)


frontpage_css = NpmBundle(
    'scss/frontpage.scss',
    depends=('scss/*.scss', ),
    filters='node-scss, cleancssurl',
    output='gen/rerodoc.frontpage.%(version)s.css',
    npm={
        "bootstrap-sass": "~3.3.5"
    }
)


def catalog(domain):
    """Return glob matching path to tranlated messages for a given domain."""
    return os.path.join(
        resource_filename('rerodoc_app', 'translations'),
        '*',  # language code
        'LC_MESSAGES',
        '{0}.po'.format(domain),
    )


i18n_js = GlobBundle(
    catalog('messages'),
    filters=AngularGettextFilter(catalog_name='rerodocTranslations'),
    output='gen/translations/rerodoc-search.js',
)


npm_js = NpmBundle(
    'js/rerodoc.search.js',
    filters='requirejs',
    output="gen/bibliomedia.npm_js.%(version)s.js",
    npm={
        'almond': '~0.3.1',
        'angular': '~1.4.8',
        'angular-loading-bar': '~0.9.0',
        'd3': '^3.5.17',
        'invenio-search-js': '~0.2.0',
        'angular-sanitize': '~1.4.10',
        'angular-gettext': '^2.3.8'
    }
)


search_js = Bundle(
    npm_js,
    i18n_js,
    # filters='jsmin',
    output='gen/rerodoc_search.%(version)s.js',
)
