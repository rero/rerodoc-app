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

"""Serializers for RERO DOC."""

from flask import json
from marshmallow import Schema, fields

from invenio_records_rest.serializers.json import JSONSerializer
from invenio_records_rest.serializers.response import record_responsify, \
    search_responsify
from invenio_records_rest.serializers.schemas.json import RecordSchemaJSONV1


class HighlightRecordSchemaJSONV1(RecordSchemaJSONV1):
    """Schema for records v1 in JSON."""

    highlight = fields.Raw()


class HighlightJSONSerializer(JSONSerializer):
    """Marshmallow based JSON serializer for records.

    Note: This serializer is not suitable for serializing large number of
    records.
    """

    @staticmethod
    def preprocess_search_hit(pid, record_hit, links_factory=None):
        """Prepare a record hit from Elasticsearch for serialization."""
        links_factory = links_factory or (lambda x: dict())
        record = dict(
            pid=pid,
            metadata=record_hit['_source'],
            links=links_factory(pid),
            revision=record_hit['_version'],
            created=None,
            updated=None,
        )
        if record_hit.get('highlight'):
            record['highlight'] = record_hit.get('highlight')
        # Move created/updated attrs from source to object.
        for key in ['_created', '_updated']:
            if key in record['metadata']:
                record[key[1:]] = record['metadata'][key]
                del record['metadata'][key]
        return record

json_v1 = HighlightJSONSerializer(HighlightRecordSchemaJSONV1)

json_v1_search = search_responsify(json_v1, 'application/json')
