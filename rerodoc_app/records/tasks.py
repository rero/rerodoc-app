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

"""Celery tasks to create records."""

from __future__ import absolute_import, print_function

import uuid

from celery import shared_task

from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_records.api import Record

from .minters import recid_minter


@shared_task(ignore_result=True)
def create_records(records):
    """Async records creation and indexing."""
    record_indexer = RecordIndexer()
    record_uuids = []
    for record in records:
        uid = uuid.uuid4()
        id = recid_minter(uid, record)
        record = Record.create(record, id_=uid)
        record_uuids.append(uid)
        db.session.flush()
    record_indexer.bulk_index(record_uuids)
    record_indexer.process_bulk_queue()
    db.session.commit()
