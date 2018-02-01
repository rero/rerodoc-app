import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator

validator = validator('common/edition-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate({
        'statement': 'Name',
        'remainder': 'Remainder'
    })


def test_from_marc():
    record = marc2record({
        '250__': {
            'a': 'Name',
            'b': 'Remainder'
        }
    })
    assert record == {
        'edition': {
            'statement': 'Name',
            'remainder': 'Remainder'
        }
    }


def test_marc2marc():
    marc = {
        '250__': {
            'a': 'Name',
            'b': 'Remainder'
        }
    }
    converted = marc2marc(marc)
    assert marc == converted


# def test_jsonld(book_context):
#     record = {
#         'recid': '1234',
#         'edition': {
#             'name': 'Name',
#             'remainder': 'Remainder'
#         }
#     }
#     converted = record2jsonld(record, book_context)
#     assert converted == [{
#         '@id': 'http://doc.rero.ch/record/1234',
#         'http://purl.org/ontology/bibo/edition': [{
#             '@value': 'Name Remainder'
#         }]
#     }]
