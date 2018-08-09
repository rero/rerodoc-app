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

from invenio_records_rest.serializers.json import JSONSerializer
from invenio_records_rest.schemas.json import RecordSchemaJSONV1
from invenio_records_rest.serializers.response import record_responsify
from invenio_records_rest.serializers.response import search_responsify
from flask import json, request, render_template
from ..dojson.utils import get_context
from rdflib import Graph
import json as native_json
from invenio_marc21.serializers.marcxml import MARCXMLSerializer \
                                               as DOJSONMARCXMLSerializer
from ..dojson.models import book2marc


class MARCXMLSerializer(DOJSONMARCXMLSerializer):
    """To do."""

    def __init__(self, dojson_model, xslt_filename=None, schema_class=None,
                 replace_refs=False):
        """."""
        self.dumps_kwargs = dict(xslt_filename=xslt_filename) if \
            xslt_filename else {}
        self.schema_class = schema_class
        super(MARCXMLSerializer, self).__init__(
            dojson_model, replace_refs=replace_refs)

    def serialize_search(self, pid_fetcher, search_result,
                         item_links_factory=None, **kwargs):
        """To do."""
        total = search_result['hits']['total']
        out = '<!--  Search-Engine-Total-Number-Of-Results: %s  -->\n' % total
        parent = super(MARCXMLSerializer, self)
        return out + parent.serialize_search(pid_fetcher, search_result,
                                             item_links_factory,
                                             **kwargs).decode('utf-8')


class LDSerializer(JSONSerializer):
    """To do."""

    def __init__(self, schema_class, output_format='json-ld',
                 replace_refs=False):
        """Initialize record."""
        self.output_format = output_format
        if output_format not in ['xml', 'json-ld', 'turtle']:
            self.output_format = 'json-ld'
        self.schema_class = schema_class
        super(LDSerializer, self).__init__(
            schema_class=schema_class, replace_refs=replace_refs)

    def dump(self, obj, context=None):
        """Serialize object with schema."""
        from pyld import jsonld
        import copy
        json_format = request.args.get('f', 'expanded')

        rec = copy.deepcopy(obj.get('metadata'))
        context = get_context('book')
        rec.update(context)
        if json_format == 'raw':
            return rec
        compacted = jsonld.compact(rec, context)
        if json_format == 'compacted':
            return compacted
        expanded = jsonld.expand(compacted)[0]

        # if self.output_format == 'json-ld':
        return expanded

    def serialize(self, pid, record, links_factory=None):
        """Serialize a single record and persistent identifier.

        :param pid: Persistent identifier instance.
        :param record: Record instance.
        :param links_factory: Factory function for the link generation,
                              which are added to the response.
        """
        obj = self.transform_record(pid, record, links_factory)
        if self.output_format == 'json-ld':
            return json.dumps(obj, indent=2)
        graph = Graph().parse(data=native_json.dumps(obj, indent=2),
                              format="json-ld")

        return graph.serialize(format=self.output_format)

    def serialize_search(self, pid_fetcher, search_result, links=None,
                         item_links_factory=None):
        """Serialize a search result.

        :param pid_fetcher: Persistent identifier fetcher.
        :param search_result: Elasticsearch search result.
        :param links: Dictionary of links to add to response.
        """
        total = search_result['hits']['total']
        to_return = []
        for hit in search_result['hits']['hits']:
            obj = self.transform_search_hit(
                    pid_fetcher(hit['_id'], hit['_source']),
                    hit,
                    links_factory=item_links_factory,
                )
            to_return.append(obj)
        if self.output_format == 'json-ld':
            to_return = json.dumps(dict(
                hits=dict(
                    hits=to_return,
                    total=total
                    )
                ))
            return native_json.dumps(to_return, indent=2)

        graph = Graph().parse(data=native_json.dumps(to_return, indent=2),
                              format="json-ld")
        # out = ''
        if self.output_format == 'xml':
            out = '<!--  Search-Engine-Total-Number-Of-Results: %s  -->\n' \
                  % total
        if self.output_format == 'turtle':
            out = '# Search-Engine-Total-Number-Of-Results: %s\n' % total
        return out + graph.serialize(format=self.output_format).decode('utf-8')

marcxml_v1 = MARCXMLSerializer(
    book2marc, schema_class=None, replace_refs=True)
marcxml_v1_search = search_responsify(marcxml_v1, 'application/marcxml+xml')
marcxml_v1_response = record_responsify(marcxml_v1, 'application/marcxml+xml')


ld_json_v1 = LDSerializer(RecordSchemaJSONV1, output_format='json-ld')
ld_turtle_v1 = LDSerializer(RecordSchemaJSONV1, output_format='turtle')
ld_xml_v1 = LDSerializer(RecordSchemaJSONV1, output_format='xml')

ld_json_v1_response = record_responsify(ld_json_v1, 'application/ld+json')
ld_json_v1_search = search_responsify(ld_json_v1, 'application/ld+json')

ld_turtle_v1_response = record_responsify(ld_turtle_v1, 'text/tutle')
ld_turtle_v1_search = search_responsify(ld_turtle_v1, 'text/turtle')

ld_xml_v1_response = record_responsify(ld_xml_v1, 'application/rdf+xml')
ld_xml_v1_search = search_responsify(ld_xml_v1, 'application/rdf+xml')
