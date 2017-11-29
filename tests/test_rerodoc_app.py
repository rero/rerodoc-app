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

"""Module tests."""

from __future__ import absolute_import, print_function

from flask import Flask

from rerodoc_app import RerodocApp


def test_version():
    """Test version import."""
    from rerodoc_app import __version__
    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask('testapp')
    ext = RerodocApp(app)
    assert 'rerodoc-app' in app.extensions

    app = Flask('testapp')
    ext = RerodocApp()
    assert 'rerodoc-app' not in app.extensions
    ext.init_app(app)
    assert 'rerodoc-app' in app.extensions


def test_view(app):
    """Test view."""
    RerodocApp(app)
    app.config.update(
        RERODOC_APP_BASE_TEMPLATE='rerodoc_app/base.html'
    )
    with app.test_client() as client:
        res = client.get("/")
        assert res.status_code == 200
        assert 'Welcome to Rerodoc-App' in str(res.data)
