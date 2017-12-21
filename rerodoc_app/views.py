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

import os
import re
from os.path import dirname, isfile, join

import markdown
import six
from elasticsearch_dsl import TermsFacet
from flask import Blueprint, Markup, abort, current_app, render_template, \
    render_template_string, request, url_for
from flask_babelex import gettext as _
from flask_menu import Menu, register_menu
from werkzeug.utils import import_string

from invenio_search import RecordsSearch

from .receivers import connect_receivers

blueprint = Blueprint(
    'rerodoc_app',
    __name__,
    template_folder='templates',
    static_folder='static',
)


connect_receivers()

@blueprint.route("/")
def index():
    """Home Page."""
    search = RecordsSearch(index='records')[0:0]
    search.aggs.bucket('institutions', 'terms', field='_collections',
                       size=0, include='RERO_DOC\.NAVSITE\.[A-Z]+')
    search.aggs.bucket('doc_type', 'terms', field='_collections',
                       size=0, include='RERO_DOC.NAVDOCTYPE\.[A-Z]+')
    # search.aggs.bucket('institutions', 'terms',
    #                    field='institution.code', size=0)
    # search.aggs.bucket('doc_type', 'terms',
    #                    field='document_type.main', size=0)
    results = search.execute()
    institutions = results.aggregations.institutions.to_dict().get('buckets')
    doc_types = results.aggregations.doc_type.to_dict().get('buckets')
    return render_template('rerodoc/index.html', institutions=institutions,
                           doc_types=doc_types, n_documents=results.hits.total)


@blueprint.route("/iheid/search")
@register_menu(blueprint, 'main.iheid', 'IHEID', order=2)
def search():
    """Search page ui."""
    filters = {
        'geneve': 'RERO_DOC.NAVSITE.GENEVE.IHEID'
    }
    return render_template(current_app.config['SEARCH_UI_SEARCH_TEMPLATE'],
                           search_hidden_params=filters,
                           search_api='/api/iheid')


@blueprint.route("/news")
@register_menu(blueprint, 'main.news', 'News', order=1)
def news():
    """To do."""
    current_language = current_app.extensions.get('invenio-i18n').language
    news_file_name = join(dirname(__file__), "data", "news",
                          "%s.md" % current_language)
    if not isfile(news_file_name):
        abort(404)
    with open(news_file_name) as news_file:
        content = Markup(markdown.markdown(news_file.read()))
    return render_template('rerodoc/news.html', content=content)


@blueprint.route("/help")
@register_menu(blueprint, 'main.help', 'Help', order=0)
def help():
    """To do."""
    current_language = current_app.extensions.get('invenio-i18n').language
    news_file_name = join(dirname(__file__), "data", "help",
                          "%s.md" % current_language)
    if not isfile(news_file_name):
        abort(404)
    with open(news_file_name) as news_file:
        content = Markup(markdown.markdown(news_file.read()))
    return render_template('rerodoc/news.html', content=content)


@blueprint.route("/help/search")
@register_menu(blueprint, 'main.help.search', 'Search', order=0)
def help_search():
    """To do."""
    current_language = current_app.extensions.get('invenio-i18n').language
    news_file_name = join(dirname(__file__), "data", "help",
                          "search_%s.md" % current_language)
    if not isfile(news_file_name):
        abort(404)
    with open(news_file_name) as news_file:
        content = Markup(markdown.markdown(news_file.read()))
    return render_template('rerodoc/news.html', content=content)


@blueprint.route("/help/glossary")
@register_menu(blueprint, 'main.help.glossary', 'Glossary', order=1)
def help_glossary():
    """To do."""
    current_language = current_app.extensions.get('invenio-i18n').language
    news_file_name = join(dirname(__file__), "data", "help"
                          "glossary_%s.md" % current_language)
    if not isfile(news_file_name):
        abort(404)
    with open(news_file_name) as news_file:
        content = Markup(markdown.markdown(news_file.read()))
    return render_template('rerodoc/news.html', content=content)


def records_ui_export(pid, record, template=None, format='json', **kwargs):
    """Record serialization view.

    Plug this method into your ``RECORDS_UI_ENDPOINTS`` configuration:

    .. code-block:: python

        RECORDS_UI_ENDPOINTS = dict(
            recid=dict(
                # ...
                route='/records/<pid_value/files/<filename>',
                view_imp='zenodo.modules.records.views.records_ui_export',
            )
        )
    """
    formats = current_app.config.get('RERODOC_RECORDS_EXPORTFORMATS')
    # fmt = request.view_args.get('format')
    if formats.get(format) is None:
        return render_template(
            'rerodoc_app/records_export_unsupported.html'), 410
    else:
        serializer = import_string(formats[format]['serializer'])
        data = serializer.serialize(pid, record)
        if isinstance(data, six.binary_type):
            data = data.decode('utf8')

        return render_template(
            template, pid=pid, record=record,
            data=data, format_title=formats[format]['title'])


@blueprint.app_template_filter()
def format_metadata(key, data, lang='en'):
    """To do."""
    value = data.get(key, '')
    if key == 'document_type':
        return _(value.get('main')).capitalize()
    if key == 'language':
        return translate_language(value, lang)
    if key == 'udc':
        return value.get(lang)
    if key == 'rero_id':
        return '<a href="%s">%s</a>' % (value, value.split('/')[-1])
    if key == 'keyword':
        to_return = []
        for keyword in value:
            to_return.append("; ".join(keyword.get('content')))
        return "<br/>".join(to_return)

    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        if value.get('full'):
            return value.get('full')
    if isinstance(value, list) and value:
        if isinstance(value[0], str):
            return ", ".join(value)
        if isinstance(value[0], dict) and value and value[0].get('full'):
            return ", ".join([v.get('full') for v in value])


@blueprint.app_template_filter()
def format_human_readable_year_month(input_date, lang="en"):
    """Converts a date in format "YYYY-MM" to a language-based "Month YYYY".

    Examples:
        format_human_readable_year_month('2010-04', 'fr') = 'Avril 2010'
        format_human_readable_year_month('2010-10', 'de') = 'Oktober 2010'

    """
    MONTH_NAMES = {
        'en': [u'January', u'February', u'March', u'April', u'May', u'June',
               u'July', u'August', u'September', u'October', u'November',
               u'December'],
        'fr': [u'Janvier', u'Février', u'Mars', u'Avril', u'Mai', u'Juin',
               u'Juillet', u'Août', u'Septembre', u'Octobre', u'Novembre',
               u'Décembre'],
        'de': [u'Januar', u'Februar', u'März', u'April', u'Mai', u'Juni',
               u'Juli', u'August', u'September', u'Oktober', u'November',
               u'Dezember'],
        'it': [u'Gennaio', u'Febbraio', u'Marzo', u'Aprile', u'Maggio',
               u'Giugno', u'Luglio', u'Agosto', u'Settembre', u'Ottobre',
               u'Novembre', u'Dicembre']
        }
    input_date = input_date.strip()
    if re.match(r'^\d{4}-\d{2}$', input_date):
        (y, m) = input_date.split('-')
        y = int(y)
        m = int(m)
        if 1 <= m <= 12:
            if MONTH_NAMES.get(lang):
                m = MONTH_NAMES.get(lang[0:2])[m-1]
            else:
                m = MONTH_NAMES.get('en')[m-1]
        else:
            return input_date
        to_return = "%s %s" % (m, y)
        return to_return.encode("utf-8")
    else:
        return input_date


@blueprint.app_template_filter()
def translate(message):
    """To do."""
    return _(message)


@blueprint.app_template_filter()
def translate_language(lang, in_lang):
    """To do."""
    from babel import Locale
    try:
        return Locale(lang).get_language_name(in_lang).capitalize()
    except:
        return lang


@blueprint.app_template_filter()
def permalink(record):
    """To do."""
    return url_for('invenio_records_ui.recid',
                   pid_value=record.get('recid'),
                   external=True)


@blueprint.app_template_filter()
def facebook(record, lang='en'):
    """To do."""
    link = 'https://www.facebook.com/sharer.php?s=100'
    url = permalink(record)
    link += "&p[url]=%s" % url
    title = record.get('title', {}).get('full')
    if title:
        link += "&p[title]=%s" % title
    summary = None
    for summ in record.get('summary', []):
        if summ.get('lang') == lang:
            summary = summ.get('content')
    if summary:
        link += "&p[summary]=%s" % summary
    # url = url_for('index')
    return link


@blueprint.app_template_filter()
def get_files_list(record):
    """To do."""
    to_return = []

    for file in record.get('_files', []):
        if file.get('filetype') == 'main':
            file_name = file.get('key')
            basename = os.path.splitext(file_name)[0]
            to_return.append({
                'file_name': file_name,
                'thumb_name': basename + '_thumb.jpg',
                'size': file.get('size')
                })
    return to_return


@blueprint.app_template_filter()
def truncate_summary(text, length=400):
    """To do."""
    if len(text) < length:
        return text
    new_text = text[0:length]

    # removed truncate word
    res = new_text.rpartition(" ")
    new_text = res[0] or res[2]
    new_text += "..."
    return new_text
