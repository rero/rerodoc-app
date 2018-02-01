import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator

validator = validator('common/content_note-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate(['Note line 1\n Line 2'])


def test_from_marc():
    record = marc2record({
        '505__': [{'a': 'Note Line 1\n Line 2'}]
    })
    assert record.get('content_note') == ['Note Line 1\n Line 2']


def test_marc2marc():
    marc = {'505__': [{'a': 'Note line 1\n Line 2'}]}
    converted = marc2marc(marc)
    assert marc == converted
