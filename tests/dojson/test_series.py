import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator
from jsonschema import ValidationError, validate

validator = validator('common/series-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate({
        'name': 'Name',
        'volume': '3'
    })


def test_from_marc():
    record = marc2record({
        '490__': {
            'a': 'Name',
            'v': '3'
        }
    })
    assert record.get('series') == {
        'name': 'Name',
        'volume': '3'
    }


def test_marc2marc():
    marc = {
        '490__': {
            'a': 'Name',
            'v': '3'
        }
    }
    converted = marc2marc(marc)
    assert marc == converted


# def test_jsonld(book_context):
#     record = {
#         'recid': '1234',
#         'series': {
#             'name': 'Name',
#             'volume': '3',
#             'full': 'Name ; 3'
#         }
#     }
#     converted = record2jsonld(record, book_context)
#     assert converted == [{
#         '@id': 'http://doc.rero.ch/record/1234',
#         'http://purl.org/dc/terms/bibliographicCitation': [{
#             '@value': 'Name ; 3'
#         }]
#     }]
