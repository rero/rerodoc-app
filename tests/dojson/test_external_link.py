import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator

validator = validator('common/external_link-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate([{
        'url': 'http://doc.rero.ch',
        'label': 'Home Page'
    }])


def test_from_marc():
    record = marc2record({
        '8564_': [{
            'u': 'http://doc.rero.ch',
            'y': '2007-11-25 23:47:43',
            'z': 'Home Page'
        }]
    })
    assert record == {
        'external_link': [{
            'url': 'http://doc.rero.ch',
            'label': 'Home Page'
        }]
    }


def test_marc2marc():
    marc = {
        '8564_': [{
            'u': 'http://doc.rero.ch',
            'z': 'Home Page'
        }]
    }
    converted = marc2marc(marc)
    assert marc == converted
