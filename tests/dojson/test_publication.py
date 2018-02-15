# -*- coding: utf-8 -*-
import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator

validator = validator('common/publication-0.0.1.json')
assert validator


# publication.year:2015
def test_validate_record():
    validator.validate({
        'location': 'Location',
        'publisher': 'Publisher',
        'date_label': '2015-2020',
        'start_date': '2015-03-12',
        'end_date': '2020-01-01'
    })


def test_from_marc():
    record = marc2record({
        '260__': {
            'a': '[Freiburg] :',
            'b': 'Zentral-Komitee S.A.C.,',
            'c': '1911 (Bern :'
        }
    })
    assert record.get('publication') == {
        'location': '[Freiburg] :',
        'publisher': 'Zentral-Komitee S.A.C.,',
        'date_label': '1911 (Bern :',
        'start_date': '1911'
    }

    record = marc2record({
        '260__': {
            'a': 'Lyon',
            'b': 'Bruyset',
            'c': 'an VIII 1800'
        }
    })
    assert record.get('publication') == {
        'location': 'Lyon',
        'publisher': 'Bruyset',
        'date_label': 'an VIII 1800',
        'start_date': '1800'
    }

    record = marc2record({
        '260__': {
            'a': 'Location',
            'b': 'Publisher',
            'c': '2015-2017',
            'e': 'Print Location',
            'f': 'Printer'
        }
    })
    assert record.get('publication') == {
        'location': 'Location',
        'publisher': 'Publisher',
        'date_label': '2015-2017',
        'start_date': '2015',
        'end_date': '2017'
    }


def test_marc2marc():
    marc = {
        '260__': {
            'a': 'Location',
            'b': 'Publisher',
            'c': '2015-',
            'e': 'Print Location',
            'f': 'Printer'
        }
    }
    converted = marc2marc(marc)
    assert marc == converted


# def test_jsonld(book_context):
#     record = {
#         'recid': '1234',
#         'publication': {
#             'location': 'Location',
#             'publisher': 'Publisher',
#             'date': '2015-',
#             'print_location': 'Print Location',
#             'printer': 'Printer'
#         }
#     }
#     converted = record2jsonld(record, book_context)
#     assert converted == [{
#         '@id': 'http://doc.rero.ch/record/1234',
#         'http://rdaregistry.info/Elements/u/publicationStatement': [{
#             '@value': 'Location Publisher 2015- Print Location Printer'
#         }]
#     }]
