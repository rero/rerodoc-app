import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator

validator = validator('common/specific_collection-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate(['Name1', 'Name2'])


def test_from_marc():
    record = marc2record({
        '982__': [{
            'a': 'CODE',
            'b': 'Collection Name',
        }]
    })
    assert record.get('specific_collection') == ['CODE;Collection Name']


def test_marc2marc():
    marc = {
        '982__': [{
            'a': 'Collection Name',
        }]
    }
    converted = marc2marc(marc)
    assert marc == converted
