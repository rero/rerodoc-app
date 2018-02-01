import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator
from jsonschema import ValidationError

validator = validator('common/reroid-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate('http://data.rero.ch/01-R1234')
    with pytest.raises(ValidationError):
        validator.validate('R1234')


def test_from_marc():
    record = marc2record({
        '035__': {'a': 'R1234'}
    })
    assert record.get('reroid') == 'http://data.rero.ch/01-R1234'


def test_marc2marc():
    marc = {'035__': {'a': 'R1234'}}
    converted = marc2marc(marc)
    assert marc == converted


def test_jsonld(book_context):
    record = {
        'recid': '1234',
        'reroid': 'http://data.rero.ch/01-R1234'
    }
    converted = record2jsonld(record, book_context)
    jsonld = [{
        '@id': 'http://doc.rero.ch/record/1234',
        'http://purl.org/dc/terms/hasFormat': [{
            '@id': 'http://data.rero.ch/01-R1234'
        }]
    }]
    assert converted == jsonld
