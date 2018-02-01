import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator

validator = validator('common/lang-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate('en')


def test_from_marc():
    record = marc2record({
        '041__': {'a': 'eng'}
    })
    assert record.get('language') == 'en'


def test_marc2marc():
    marc = {'041__': {'a': 'eng'}}
    converted = marc2marc(marc)
    assert marc == converted


def test_jsonld(book_context):
    record = {
        'recid': '1234',
        'language': 'en'
    }
    converted = record2jsonld(record, book_context)
    jsonld = [{
        '@id': 'http://doc.rero.ch/record/1234',
        'http://purl.org/dc/terms/language': [{
            '@value': 'en'
        }]
    }]
    assert converted == jsonld
