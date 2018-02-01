import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator

validator = validator('common/recid-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate('1234')


def test_from_marc():
    record = marc2record({
        '001': '1234'
    })
    assert record.get('recid') == '1234'


def test_marc2marc():
    marc = {'001': ['1234']}
    converted = marc2marc(marc)
    assert marc == converted


def test_jsonld(book_context):
    record = {
        'recid': '1234',
        'reroid': 'http://data.rero.ch/01-R1234'
    }
    converted = record2jsonld(record, book_context)
    assert converted[0].get('@id') == 'http://doc.rero.ch/record/1234'
