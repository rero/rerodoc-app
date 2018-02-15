# -*- coding: utf-8 -*-

"""rerodoc base Invenio configuration."""

from __future__ import absolute_import, print_function

import json
import os
import sys
import uuid

import click
import six
from flask import current_app
from flask_cli import with_appcontext
from invenio_base.app import create_cli
from invenio_db import db
from invenio_files_rest.models import Bucket, Location
from invenio_indexer.api import RecordIndexer
from invenio_indexer.tasks import process_bulk_queue
from invenio_pidstore.models import PersistentIdentifier, PIDStatus
from invenio_records_files.models import RecordsBuckets

from .records.utils import extract_text, generate_thumbnail, \
    load_records_with_files


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
@click.option('-v', '--verbose',
              help='Verbosity i.e. -vvv (default: no)', count=True)
@click.option('--cache/--no-cache',
              help='use cache for files (default: yes)', default=True)
@click.option('--files/--no-files',
              help='attach fulltext files (default: yes)', default=True)
@click.option('--skip/--no-skip',
              help='skip invalid record (default: stop on error)',
              default=False)
@click.option('-m', '--max',
              help='max records to load (default: no limit)', type=int)
def load(source, verbose, cache, files, skip, max=None):
    """Load records attach files and index them."""
    data = json.load(source)
    if isinstance(data, dict):
        data = [data]

    # to upload remote fulltext files
    upload_dir = os.path.join(current_app.instance_path, 'uploads')
    try:
        os.makedirs(upload_dir)
    except FileExistsError:
        pass

    # initialize file location if needed
    if not Location.get_default():
        data_dir = os.path.join(current_app.instance_path, 'files')
        db.session.add(Location(name='default', uri='file://'+data_dir,
                                default=True))
        db.session.commit()

    # create records and index them
    click.secho('Creating records...', fg='green')
    rec_uuids = load_records_with_files(data, upload_dir, max, verbose,
                                        files, cache, skip)
    click.secho('Put %d records for indexing...' % len(rec_uuids),
                fg='green')
    RecordIndexer().bulk_index(rec_uuids)
    click.secho('Execute "run" command to process the queue!', fg='yellow')


@utils.command()
@with_appcontext
@click.argument('recid')
@click.option('-v', '--verbose', count=True)
def get_files(recid, verbose):
    """To do."""
    resolver = Resolver('recid', 'rec', Record.get_record)
    uuid, rec = resolver.resolve(recid)
    import pprint
    click.echo(json.dumps(rec.files.dumps(), indent=2))


@utils.command()
@with_appcontext
@click.argument('source', type=click.File('r'), default=sys.stdin)
@click.option('-v', '--verbose', count=True)
def compile_schema(source, verbose):
    """Resolve $ref in a jsonschema file."""
    import jsonref
    from jsonref import JsonLoader
    import jsonschema

    class TestJSONResolver(JsonLoader):

        def __init__(self, store=(), cache_results=True):
            return super(TestJSONResolver, self).__init__(store, cache_results)

        def __call__(self, uri, **kwargs):
            from invenio_jsonschemas import current_jsonschemas
            from invenio_jsonschemas.errors import JSONSchemaNotFound
            try:
                return current_jsonschemas.get_schema(uri)
            except JSONSchemaNotFound:
                return super(TestJSONResolver, self).__call__(uri, *kwargs)
    resolved_schema = jsonref.load(source, loader=TestJSONResolver())
    jsonschema.Draft4Validator.check_schema(resolved_schema)
    click.echo(json.dumps(resolved_schema, indent=2))
