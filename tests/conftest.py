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

"""Pytest configuration."""

from __future__ import absolute_import, print_function

import shutil
import tempfile

import pytest
from flask import Flask
from flask_babelex import Babel


def pytest_addoption(parser):
    """To Do."""
    parser.addoption("--runslow", action="store_true",
                     help="Run also slow tests")


@pytest.fixture()
def contributor():
    """Full contributor example."""
    return {
        'contributor': [{
            'name': '<lastname1>, <fistname1>',
            'birth_date': '1971',
            'affiliation': '<affiliation1>',
            'type': 'person',
            'role': 'author',
            'orcid': 'http://orcid.org/0000-0001-8368-5460'
        }, {
            'name': '<lastname2>, <fistname2>',
            'birth_date': '1941',
            'death_date': '1978',
            'role': 'thesis director',
            'affiliation': '<affiliation2>',
            'type': 'person'
        }, {
            'name': '<lastname3>, <fistname3>',
            'birth_date': '1974-01-01',
            'affiliation': '<affiliation3>',
            'role': 'thesis codirector',
            'type': 'person'
        }, {
            'name': '<lastname4>, <fistname4>',
            'birth_date': '1974',
            'role': 'editor',
            'type': 'person'
        }, {
            'name': '<name1>',
            'type': 'corporate',
            'role': 'author'
        }, {
            'name': '<name2>',
            'type': 'corporate',
            'role': 'author'
        }, {
            'name': '<name3>',
            'type': 'corporate',
            'role': 'printer'
        }]
    }


@pytest.yield_fixture()
def instance_path():
    """Temporary instance path."""
    path = tempfile.mkdtemp()
    yield path
    shutil.rmtree(path)


@pytest.fixture()
def base_app(instance_path):
    """Flask application fixture."""
    app_ = Flask('testapp', instance_path=instance_path)
    app_.config.update(
        SECRET_KEY='SECRET_KEY',
        TESTING=True,
    )
    Babel(app_)
    return app_


@pytest.yield_fixture()
def app(base_app):
    """Flask application fixture."""
    with base_app.app_context():
        yield base_app
