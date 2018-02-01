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

"""Marc21 to json transformation for RERO DOC."""

from __future__ import absolute_import, print_function

import re

from dojson import Overdo, utils
from dojson.utils import force_list

marc21tojson = Overdo()


@marc21tojson.over('title', '^245..')
@utils.ignore_value
def marc21totitle(self, key, value):
    """Get title.

    title: 245$a
    """
    titles = []
    main_title = value.get('a')
    if main_title:
        titles.append(main_title)
    sub_title = value.get('b', '')
    if sub_title:
        titles.append(sub_title)

    return ': '.join(titles)


@marc21tojson.over('external_oai_id', '^0248.')
@utils.ignore_value
def marc21tooai(self, key, value):
    """Get OAI External ID."""
    return value.get('a')
