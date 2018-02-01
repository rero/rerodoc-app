import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator
from jsonschema import ValidationError

validator = validator('book/isbn-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate('2-88147-009-2')
    validator.validate('9782882250209')

    with pytest.raises(ValidationError):
        validator.validate('2-88147-009')


def test_from_marc():
    record = marc2record({
        '020__': {
            'a': '2-88147-009-2'
        }
    })
    assert record.get('isbn') == '9782881470097'


def test_marc2marc():
    marc = {'020__': {'a': '9782882250209'}}
    converted = marc2marc(marc)
    assert marc == converted


def test_jsonld(book_context):
    record = {
        'recid': '1234',
        'isbn': '9782882250209'
    }
    converted = record2jsonld(record, book_context)
    assert converted == [{
        '@id': 'http://doc.rero.ch/record/1234',
        'http://purl.org/ontology/bibo/isbn13': [{
            '@value': '9782882250209'
        }]
    }]
