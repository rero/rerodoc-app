import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator
from jsonschema import ValidationError

validator = validator('common/udc-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate('004')

    validator.validate('93/94')

    validator.validate('614.253.1')

    validator.validate('81`28')

    with pytest.raises(ValidationError):
        validator.validate("81'28")

    with pytest.raises(ValidationError):
        validator.validate('614.253.544')

    validator.validate('615.84')


def test_from_marc():
    record = marc2record({
        '080__': {'a': '004'}
    })
    assert record.get('udc') == '004'


def test_marc2marc():
    marc = {'080__': {'a': '004'}}
    converted = marc2marc(marc)
    assert marc == converted


# def test_jsonld(book_context):
#     record = {
#         'recid': '1234',
#         'udc': {
#             'code': '004',
#             'en': 'Computer science',
#             'fr': 'Informatique',
#             'de': 'Informatik',
#             'it': "Informatique",
#             'uri': ['http://udcdata.info/013566']
#         }
#     }
#     converted = record2jsonld(record, book_context)
#     jsonld = [{
#         '@id': 'http://doc.rero.ch/record/1234',
#         'http://purl.org/dc/terms/subject': [{
#             '@id': 'http://udcdata.info/013566'
#         }]
#     }]
#     assert converted == jsonld
