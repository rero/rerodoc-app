import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator
from jsonschema import ValidationError

validator = validator('common/other_title-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate([{
        'main': 'Other Title',
        'sub': 'Other Subtitle',
        'language': 'en'
    }])
    with pytest.raises(ValidationError):
        validator.validate([{
            'other_title': {
                'language': 'eng'
            }
        }])


def test_from_marc():
    record = marc2record({
        '246__': {
            'a': 'Other Title',
            '9': 'eng'
        }
    })
    assert record == {
        'other_title': [{
            'main': 'Other Title',
            'language': 'en'
        }]
    }
    record = marc2record({
        '246__': {
            'a': 'Other Title',
            'b': 'Subtitle',
            '9': 'eng'
        }
    })
    assert record == {
        'other_title': [{
            'main': 'Other Title',
            'sub': 'Subtitle',
            'language': 'en'
        }]
    }


def test_marc2marc():
    marc = {
        '246__': [{
            'a': 'Other Title',
            '9': 'eng'
        }]
    }
    converted = marc2marc(marc)
    assert marc == converted


# def test_jsonld(book_context):
#     record = {
#         'recid': '1234',
#         'other_title': [{
#             'main': 'Other Title',
#             'language': 'en'
#         }]
#     }
#     converted = record2jsonld(record, book_context)
#     jsonld = [{
#         '@id': 'http://doc.rero.ch/record/1234',
#         'http://purl.org/dc/terms/alternative': [{
#             '@value': 'Other Title',
#             '@language': 'en'
#         }]
#     }]
#     assert converted == jsonld
