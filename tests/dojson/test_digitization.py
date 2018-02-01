import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator

validator = validator('common/digitization-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate({
        'location': 'Location',
        'digitizer': 'Agency',
        'date': '2015'
    })


def test_from_marc():
    record = marc2record({
        '533__': {
            'a': 'Type',
            'b': 'Location',
            'c': 'Agency',
            'd': '2015.'
        }
    })
    assert record.get('digitization') == {
        'location': 'Location',
        'digitizer': 'Agency',
        'date': '2015.'
    }


def test_marc2marc():
    marc = {
        '533__': {
            'a': 'Electronic reproduction',
            'b': 'Location',
            'c': 'Agency',
            'd': '2015.'
        }
    }
    converted = marc2marc(marc)
    assert marc == converted
