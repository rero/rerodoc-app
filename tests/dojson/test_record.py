import pytest


def test_get_wrong_context():
    from rerodoc_app.records.dojson.utils import get_context
    assert get_context("not_exists") is None
