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

"""RERO DOC query configuration."""

from functools import partial

from elasticsearch_dsl.query import Q

from invenio_records_rest.query import default_search_factory


def rerodoc_search_factory(self, search, **kwargs):
    """To do."""
    search, urlkwargs = default_search_factory(self, search, **kwargs)
    search = search.highlight('fulltext', require_field_match=False,
                              number_of_fragments=3)
    search = search.source(exclude=["fulltext"])
    return search, urlkwargs

search_factory = partial(
        rerodoc_search_factory,
        query_parser=lambda qstr: Q('query_string',
                                    query=qstr) if qstr else Q()
    )
