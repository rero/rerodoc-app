import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator

validator = validator('common/keyword-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate([{
        'language': 'en',
        'value': ['keyword1', 'keyword2']
    }])


def test_from_marc():
    record = marc2record({
        '695__': [{
            '9': 'eng',
            'a': 'keyword1 ; keyword2'
        }]
    })
    assert record == {
        'keyword': [{
            'language': 'en',
            'value': ['keyword1', 'keyword2']
        }]
    }

    record = marc2record({
        '695__': [{
            '9': 'eng',
            'a': 'keyword1 ; keyword2 ; '
        }]
    })
    assert record == {
        'keyword': [{
            'language': 'en',
            'value': ['keyword1', 'keyword2']
        }]
    }


def test_marc2marc():
    marc = {
        '695__': [{
            '9': 'eng',
            'a': 'keyword1 ; keyword2'
        }]
    }
    converted = marc2marc(marc)
    assert marc == converted
