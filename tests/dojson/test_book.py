# -*- coding: utf-8 -*-
import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator

validator = validator('records/book-v0.0.1.json')
assert validator


def test_validate_minimal_record():
    validator.validate({
        '$schema': 'http://doc.test.rero.ch/schema/book-v0.0.1.json',
        'recid': '1234',
        'title': [{
            'main': 'Main Title',
            'language': 'en'
        }],
        'language': 'en'
    })


def test_validate_full_record():
    validator.validate({
        '$schema': 'http://doc.test.rero.ch/schema/book-v0.0.1.json',
        'recid': '1234',
        'isbn': '9782882250209',
        'reroid': 'http://data.rero.ch/01-R1234',
        'title': [{
            'main': 'Maintitle',
            'sub': 'Subtitle',
            'language': 'en'
        }, {
            'main': 'Titre principal',
            'sub': 'Titre secondaire',
            'language': 'fr'
        }],
        'other_title': [{
            'main': 'Other Title',
            'sub': 'Other Subtitle',
            'language': 'en'
        }, {
            'main': 'Autre titre',
            'sub': 'Autre titre secondaire',
            'language': 'fr'
        }],
        'language': 'en',
        'contributor': [{
            'name': 'LastName, FirstName',
            'birth_date': '1971',
            'death_date': '2001',
            'role': 'author',
            'affiliation': 'Université de Fribourg',
            'orcid': 'http://orcid.org/0000-0001-8368-5460',
            'type': 'person'
        }, {
            'name': 'LastName, FirstName',
            'birth_date': '1971',
            'death_date': '2001',
            'role': 'thesis director',
            'type': 'person'
        }, {
            'name': 'Corporate',
            'role': 'editor',
            'type': 'corporate'
        }],
        'access_restriction': 'No access until 2015-01-01',
        'content_note': ['Note1', 'Note2'],
        'note': ['Note line 1\n Line 2'],
        'publication': {
            'location': 'Location',
            'publisher': 'Publisher',
            'date_label': '2015-2020',
            'start_date': '2015-03-12',
            'end_date': '2020-01-01',
        },
        'print': {
            'location': 'Geneva',
            'printer': 'Imprimeurs de Genève'
        },
        'edition': {
            'statement': 'Edition Name',
            'remainder': 'Remainder'
        },
        'other_edition': [{
            'type': 'published version',
            'url': 'http://dx.doi.org/10.1111/j.1365-3032.2012.00840.x'
        }],
        'digitization': {
            'location': 'Location',
            'digitizer': 'Agency',
            'date': '2015'
        },
        'meeting': {
            'name': 'Name',
            'location': 'Location',
            'date': '2015',
            'number': '34'
        },
        'series': {
            'name': 'Name',
            'volume': '3'
        },
        'summary': [{
            'language': 'en',
            'value': 'Summary Line 1\n Line2'
        }],
        'udc': '614.253.1',
        'keyword': [{
            'language': 'en',
            'value': ['keyword1', 'keyword2']
        }],
        'imported_keyword': [{
            'language': 'fr',
            'vocabulary': 'rero',
            'value': ['keyword1', 'keyword2']
        }],
        'institution': 'medvs',
        'type': {
            'main': 'book',
            'sub': 'book_proceed'
        },
        'document': [{
            'name': 'file_name.pdf',
            'mime': 'application/pdf',
            'size': 1014,
            'url': 'http://doc.rero.ch/record/file_name.pdf',
            'label': 'Main file',
            'number_of_pages': 100,
            'duration': 60,
            'physical_description': {
                'extent': '100 p.',
                'detail': 'ill.',
                'dimension': '25 x 30 cm'
            }
        }],
        'external_link': [{
            'url': 'http://doc.rero.ch',
            'label': 'Home Page'
        }],
        'specific_collection': ['Name1', 'Name2']
    })
