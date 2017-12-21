# -*- coding: utf-8 -*-

"""rerodoc base Invenio configuration."""

from __future__ import absolute_import, print_function

import json
import os
import sys
import uuid

import click
import PyPDF2
import six
import slate3k as slate
from flask import current_app
from flask_cli import with_appcontext

from invenio_base.app import create_cli
from invenio_db import db
from invenio_files_rest.models import Bucket, Location
from invenio_indexer.api import RecordIndexer
from invenio_indexer.tasks import process_bulk_queue
from invenio_oaiserver.minters import oaiid_minter
from invenio_pidstore.errors import PIDDoesNotExistError
from invenio_pidstore.models import PersistentIdentifier, PIDStatus
from invenio_pidstore.resolver import Resolver
from invenio_records_files.api import Record
from invenio_records_files.models import RecordsBuckets


@click.group()
def utils():
    """Utilities commands."""


@utils.command()
@with_appcontext
def list_routes():
    """To do."""
    import urllib
    from flask import current_app

    output = []

    def print_routes(app):
        for rule in app.url_map.iter_rules():
            methods = ','.join(rule.methods)
            line = urllib.parse.unquote("{:50s} {:20s} {}".format(
                   rule.endpoint, methods, rule))
            output.append(line)

        for line in sorted(output):
            click.echo(line)
    click.echo('--- main ---')
    print_routes(current_app)
    click.echo('--- api ---')
    print_routes(current_app.wsgi_app.mounts.get('/api'))


@utils.command()
@with_appcontext
@click.argument('index')
@click.argument('name')
@click.option('-v', '--verbose', count=True)
def alias(index, name, verbose):
    """To do."""
    from invenio_search.proxies import current_search_client
    current_search_client.indices.put_alias(
        index=index,
        name=name
        )
    click.secho('alias: %s added to index: %s' % (name, index), fg='green')


@utils.command()
@with_appcontext
@click.argument('source', type=click.File('r'), default=sys.stdin)
@click.option('-v', '--verbose', count=True)
@click.option('-m', '--max', type=int)
def load(source, verbose, max=None):
    """Load records and index."""
    data = json.load(source)
    if isinstance(data, dict):
        data = [data]

    resolver = Resolver('recid', 'rec', Record.get_record)

    upload_dir = os.path.join(current_app.instance_path, 'uploads')
    try:
        os.makedirs(upload_dir)
    except FileExistsError:
        pass

    if not Location.get_default():
        data_dir = os.path.join(current_app.instance_path, 'files')
        db.session.add(Location(name='default', uri='file://'+data_dir,
                                default=True))
        db.session.commit()

    click.secho('Creating records...', fg='green')
    rec_uuids = []
    n = 0
    for item in data:
        if max and n >= max:
            break
        if not item.get('document'):
            if verbose > 1:
                click.secho('Warning: %s do not contains document'
                            % item.get('recid'), fg='red')
            continue

        if not item.get('recid'):
            click.secho('Error records do not contains recid!', fg='red')

        recid = item.get('recid')

        # record already exists in db?
        try:
            rec_uuid, rec = resolver.resolve(recid)
            if verbose > 1:
                click.secho('%s record already exists' % recid, fg='yellow')
            rec_uuids.append(str(rec_uuid.object_uuid))
            n += 1
            continue
        # create new record
        except PIDDoesNotExistError:
            # generate a new uuid
            rec_uuid = uuid.uuid4()
            print(rec_uuid)
            # create mapping between recid and uuid
            pid = PersistentIdentifier.create(
                'recid', recid, object_type='rec', object_uuid=rec_uuid,
                status=PIDStatus.REGISTERED)
            # create Record
            rec = Record.create(item, id_=rec_uuid)
            bucket = Bucket.create()
            record_buckets = RecordsBuckets.create(record=rec.model,
                                                   bucket=bucket)

        oaiid_minter(rec_uuid, rec)
        out_dir = os.path.join(upload_dir, recid)
        try:
            os.makedirs(out_dir)
        except FileExistsError:
            pass

        rec_uuids.append(str(rec_uuid))
        for doc in rec.get('document'):
            from urllib.request import urlretrieve
            from urllib.error import HTTPError
            file_name = os.path.join(out_dir,
                                     doc.get('url').split('/')[-1])
            if not os.path.isfile(file_name):
                try:
                    if verbose > 1:
                        click.secho('try to upload: %s' % doc.get('url'),
                                    fg='green')
                    file_name, request = urlretrieve(doc.get('url'),
                                                     file_name)
                except HTTPError:
                    click.secho('upload error: %s' % (doc.get('url')),
                                fg='red')
            elif verbose > 1:
                click.secho('%s already exists' % file_name, fg='yellow')

            rec.files[doc.get('name')] = open(file_name, 'rb')
            rec.files[doc.get('name')]['filetype'] = 'main'

            if doc.get('mime') == 'application/pdf':
                thumb_filename = doc.get('name').replace('.pdf', '')
                thumb_filename += '_thumb.jpg'
                thumb_filepath = os.path.join(out_dir, thumb_filename)
                if not os.path.isfile(thumb_filepath):
                    if verbose > 1:
                        click.secho('try to generate %s' % thumb_filepath,
                                    fg='yellow')
                    generate_thumbnail(file_name, thumb_filepath)

                rec.files[thumb_filename] = open(thumb_filepath, 'rb')
                file_obj = rec.files[thumb_filename]
                rec.files[thumb_filename]['filetype'] = 'thumb'

                text_filename = doc.get('name').replace('.pdf', '.txt')
                text_filepath = os.path.join(out_dir, text_filename)
                if not os.path.isfile(text_filepath):
                    if verbose > 1:
                        click.secho('try to generate %s' % text_filepath,
                                    fg='yellow')
                    extract_text(file_name, text_filepath)
                if os.path.getsize(text_filepath):
                    rec.files[text_filename] = open(text_filepath, 'rb')
                    file_obj = rec.files[text_filename]
                    rec.files[text_filename]['filetype'] = 'raw_text'
                else:
                    if verbose > 2:
                        click.secho('%s has zero size' % text_filename)
            rec.commit()
        db.session.commit()
        n += 1

    # db.session.commit()
    click.secho('Put %d records for indexing...' % len(rec_uuids),
                fg='green')
    # click.secho('Execute "run" command to process the queue!', fg='yellow')
    RecordIndexer().bulk_index(rec_uuids)
    click.secho('Bulk indexing...', fg='green')
    RecordIndexer().process_bulk_queue()


def generate_thumbnail(filename, outfilename):
    """To do."""
    from wand.image import Image
    img = Image(filename='%s[0]' % filename, resolution=100)
    img.transform(resize='150x150>')
    img.save(filename=outfilename)


def extract_text(filename, outfilename):
    """To do."""
    with open(filename, 'rb') as f:
        try:
            # doc = slate.PDF(f)
            doc = PyPDF2.PdfFileReader(f)
            text = []
            for np in range(doc.getNumPages()):
                page = doc.getPage(np)
                text.append(page.extractText())
        except:
            open(outfilename, 'wb')
            return
    # if not doc.text():
    #    return None
    with open(outfilename, 'wb') as of:
        of.write(bytes(" ".join(text), 'utf-8'))


@utils.command()
@with_appcontext
@click.argument('recid')
@click.option('-v', '--verbose', count=True)
def get_files(recid, verbose):
    """To do."""
    resolver = Resolver('recid', 'rec', Record.get_record)
    uuid, rec = resolver.resolve(recid)
    import pprint
    pprint.pprint(rec.files.dumps())
