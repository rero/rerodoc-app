import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator

validator = validator('common/meeting-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate({
        'name': 'Name',
        'location': 'Location',
        'date': '2015',
        'number': '34'
    })


def test_from_marc():
    record = marc2record({
        '711__': {
            'a': 'Name',
            'c': 'Location',
            'd': '2015',
            'n': '34'
        }
    })
    assert record.get('meeting') == {
        'name': 'Name',
        'location': 'Location',
        'date': '2015',
        'number': '34'
    }


def test_marc2marc():
    marc = {
        '711__': {
            'a': 'Name',
            'c': 'Location',
            'd': '2015',
            'n': '34'
        }
    }
    converted = marc2marc(marc)
    assert marc == converted


# def test_jsonld(book_context):
#     record = {
#         'recid': '1234',
#         'meeting': {
#             'name': 'Name',
#             'location': 'Location',
#             'date': '2015',
#             'number': '34'
#         }
#     }
#     converted = record2jsonld(record, book_context)
#     assert converted == [{
#         '@id': 'http://doc.rero.ch/record/1234',
#         'http://purl.org/dc/elements/1.1/contributor': [{
#             '@value': 'Name (34 : 2015 : Location)'
#         }]
#     }]
