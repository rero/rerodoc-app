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

"""RERO DOC Invenio records utilities."""

import os
import uuid
from urllib.error import HTTPError
from urllib.request import urlretrieve

import click
from flask import current_app
from invenio_db import db
from invenio_files_rest.models import Bucket
from invenio_oaiserver.minters import oaiid_minter
from invenio_pidstore.errors import PIDDoesNotExistError
from invenio_pidstore.models import PersistentIdentifier
from invenio_pidstore.resolver import Resolver
from invenio_records_files.api import Record
from invenio_records_files.models import RecordsBuckets
from jsonschema.exceptions import ValidationError


class Logger(object):
    """Simple verbose level storage."""

    verbose = 2


def warning(msg):
    """Warning log message."""
    current_app.logger.warning(msg)
    if Logger.verbose > 1:
        click.secho(msg, fg='blue')


def error(msg):
    """Error log message."""
    current_app.logger.error(msg)
    if Logger.verbose > 0:
        click.secho(msg, fg='red')


def info(msg):
    """Info log message."""
    current_app.logger.info(msg)
    if Logger.verbose > 2:
        click.secho(msg, fg='green')


def load_records_with_files(records, upload_dir, max=0, verbose=0, files=True,
                            cache=True, skip=False):
    """Load records with files support.

       It also:
         - create thumbnail for pdf
         - extract text for pdf
         - append files to the bibliographic record

    :param records: list of records in JSON format.
    :param upload_dir: directory for temporary files will be used for cache.
    :param max: max records to load.
    :param verbose: verbose level.
    :param files: attach files if True.
    :param cache: use cache if True.
    :param skip: skip invalid records.
    :returns: list of touched uuids for indexing.
    """
    Logger.verbose = verbose
    rec_uuids = []
    n = 0
    resolver = Resolver('recid', 'rec', Record.get_record)
    if not files:
        warning('files are ignored')
    # stop if max record is reached
    if max:
        records = records[:max]
    count = len(records)
    click.secho(
        'Starting loading {0} record ...'.format(
            len(records)),
        fg='green')

    with click.progressbar(records, length=count) as bar:
        for record in bar:

            # ignore record if does not contains document
            if not record.get('document'):
                if verbose > 1:
                    warning('%s do not contains document'
                            % record.get('recid'))
                continue
            recid = record.get('recid', '-1')
            if recid:
                info('record: %s detected...' % recid)
            update = True
            try:
                # record already exists in db?
                try:
                    pid, rec = resolver.resolve(recid)
                    rec_uuid = pid.object_uuid
                    info('record: %s exists, updating...' % recid)
                    rec.update(record)
                    rec.commit()
                # create new record
                except PIDDoesNotExistError:
                    update = False
                    # generate a new uuid
                    rec_uuid = uuid.uuid4()
                    # create mapping between recid and uuid
                    pid = PersistentIdentifier.create('recid', recid,
                                                      object_type='rec',
                                                      object_uuid=rec_uuid)
                    # create Record
                    rec = Record.create(record, id_=rec_uuid)

                    bucket = Bucket.create()
                    RecordsBuckets.create(record=rec.model,
                                          bucket=bucket)
                    pid.register()
                    info('%s record created' % rec.get('recid'))
                    oaiid_minter(rec_uuid, rec)
                if files:
                    rec_upload_dir = os.path.join(upload_dir, recid)
                    try:
                        os.makedirs(rec_upload_dir)
                    except FileExistsError:
                        pass
                    for document in record.get('document'):
                        file_name = upload_file(document.get('url'),
                                                rec_upload_dir,
                                                force=not cache)
                        if file_name:
                            name = document.get('name')
                            rec.files[name] = open(file_name, 'rb')
                            rec.files[name]['filetype'] = 'main'
                            append_thumbnail(rec, document, rec_upload_dir,
                                             not cache)
                            append_extracted_text(rec, document,
                                                  rec_upload_dir,
                                                  not cache)
                            rec.commit()
            except ValidationError as e:
                if not update:
                    pid.delete()
                else:
                    info('Record %s untouched' % recid)
                error('Invalid record (%s)' % recid)
                warning('Validation error: %s' % e)
                if not skip:
                    raise e
                continue
            else:
                db.session.flush()
                # touched record
                rec_uuids.append(rec_uuid)
                n += 1
        db.session.commit()
    return rec_uuids


def append_extracted_text(record, document, upload_dir, force=False):
    """Add fulltext to record."""
    if document.get('mime') == 'application/pdf':
        name = document.get('name')
        text_filename = name.replace('.pdf', '.txt')
        text_filepath = os.path.join(upload_dir, text_filename)
        if text_filename not in record.files.keys or force:
            if not os.path.isfile(text_filepath) or force:
                main_file = record.files[name].file.storage().open()
                n_char = extract_text(main_file, text_filepath)
                info('%s characters extracted into %s'
                     % (n_char, text_filepath))
        if os.path.isfile(text_filepath) and os.path.getsize(text_filepath):
            record.files[text_filename] = open(text_filepath, 'rb')
            record.files[text_filename]['filetype'] = 'raw_text'
        else:
            return None
        return text_filename
    return None


def append_thumbnail(record, document, upload_dir, force=False):
    """Add thumbnail to a given record."""
    if document.get('mime') == 'application/pdf':
        name = document.get('name')
        thumb_filename = name.replace('.pdf', '_thumb.jpg')
        if thumb_filename not in record.files.keys or force:
            thumb_filepath = os.path.join(upload_dir, thumb_filename)
            pdf_filepath = os.path.join(upload_dir, name)
            if not os.path.isfile(thumb_filepath) or force:
                generate_thumbnail(pdf_filepath, thumb_filepath)
                info('%s generated!' % thumb_filename)
            if os.path.isfile(thumb_filepath):
                record.files[thumb_filename] = open(thumb_filepath, 'rb')
                record.files[thumb_filename]['filetype'] = 'thumb'
        else:
            warning('%s aleary exists!' % thumb_filename)
        return thumb_filename


def upload_file(url, upload_dir, force=False):
    """Upload a remote file."""
    file_name = os.path.join(upload_dir,
                             url.split('/')[-1])
    if not os.path.isfile(file_name) or force:
        try:
            file_name, request = urlretrieve(url, file_name)
            return file_name
        except HTTPError:
            error('%s upload failed!' % url)
            return False
    info('%s alredy exists using cache' % file_name)
    return file_name


def generate_thumbnail(filename, outfilename=None):
    """Generate a thumnail for a given pdf filename."""
    # img = Image(filename=filename+'[0]', resolution=20)
    # try:
    #     img.alpha_channel = 'off'
    #     img.transform(resize='150x150>')

    from invenio_multivio.pdf.api import PDF
    try:
        pdf = PDF(path=filename, page_nr=0)
        pdf.load()
        img = pdf.render_page(max_width=80, max_height=80)

    except Exception:
        error('image generation failed')
        return None
    if outfilename:
        return img.save(filename=outfilename)
    return img


def extract_text(file, outfilename=None):
    """Extract fulltext from a given pdf file."""
    from invenio_multivio.pdf.api import PDF
    text = []
    try:
        pdf = PDF(path=file)
        pdf.load()
        text = pdf.get_text_page()
        # doc = slate.PDF(file)
        # doc = PyPDF2.PdfFileReader(file)
        # if doc.isEncrypted:
        #     warning('file is encrypted')
        #     return []
        # text = []
        # for np in range(doc.getNumPages()):
        #     page = doc.getPage(np)
        #     text.append(page.extractText())
    except Exception:
        error('text generation failed')
        pass
    if not text:
        warning('%s: do not contains text' % file)
        return text
    if outfilename:
        with open(outfilename, 'wb') as of:
            return of.write(bytes(" ".join(text), 'utf-8'))
    return text


def get_file(url):
    """Return a file path given an URL.

    Used by invenio-multivio.
    """
    import re
    from invenio_pidstore.resolver import Resolver
    from invenio_records_files.api import Record
    regex = re.search(r'doc.rero.ch/record/(\w+)/files/(.*)', url)
    pid, filename = regex.groups()
    resolver = Resolver('recid', 'rec', Record.get_record)
    pid, record = resolver.resolve(pid)
    storage = record.files[filename].obj.file.storage()
    return storage.fileurl.replace('file://', '')
