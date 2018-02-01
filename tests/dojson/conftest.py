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

"""Fixtures for tests."""

import json
import os

import jsonschema
import pytest
from pkg_resources import resource_filename


def validator(schema):
    """To Do."""
    schema = resource_filename('rerodoc_app.records.jsonschemas', schema)

    schema_dir = resource_filename('rerodoc_app.records.jsonschemas', '')
    schema_name = os.path.basename(schema)

    with open(schema) as f:
        schema_json = json.load(f)

    # check if schema is valid
    jsonschema.Draft4Validator.check_schema(schema_json)

    resolver = jsonschema.RefResolver(
        'file://' + schema_dir + '/', schema_name
    )

    validator = jsonschema.Draft4Validator(
        schema_json, resolver=resolver, types=(('array', (list, tuple)), )
    )

    return validator


def marc2record(marc, record_type='book'):
    """To Do."""
    from rerodoc_app.records.dojson import book, audio
    if record_type == 'book':
        return book.do(marc)
    if record_type == 'audio':
        return audio.do(marc)


def marc2marc(marc, record_type='book'):
    """To Do."""
    from rerodoc_app.records.dojson import book, book2marc
    from rerodoc_app.records.dojson import audio, audio2marc
    if record_type == 'book':
        record = book.do(marc)
        return book2marc.do(record)
    if record_type == 'audio':
        record = audio.do(marc)
        return audio2marc.do(record)


def record2jsonld(record, context):
    """To Do."""
    from pyld import jsonld
    import json
    import rdflib_jsonld
    from rdflib import Graph
    import copy
    rec = copy.deepcopy(record)
    rec.update(context)
    compacted = jsonld.compact(rec, context)
    return jsonld.expand(compacted)


def get_demo_record(rec):
    """Get a record in Json format from a MarcXML."""
    from dojson.contrib.marc21.utils import create_record
    from rerodoc_app.records.dojson import book
    blob = create_record(rec)
    data = book.do(blob)
    return data


@pytest.fixture(scope='session')
def simple_book_record():
    """A sample book record."""
    return get_demo_record(file(os.path.join(os.path.dirname(__file__),
                                             "book_record.xml")).read())


@pytest.fixture(scope='session')
def book_schema():
    """Session-wide book schema."""
    from rerodoc_app.dojson.utils import get_schema
    return get_schema("book")


@pytest.fixture(scope='session')
def book_context():
    """Session-wide book context."""
    from rerodoc_app.records.dojson.utils import get_context
    return get_context("book")
