import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator
from jsonschema import ValidationError

validator = validator('common/document-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate([{
        'name': 'file_name.pdf',
        'mime': 'application/pdf',
        'size': 1014,
        'url': 'http://doc.rero.ch/record/file_name.pdf',
        'label': 'Main file',
        'number_of_pages': 100,
        'duration': 60,
        'physical_description': {
            'extent': '100 p.',
            'details': 'ill.',
            'dimensions': '25 x 30 cm'
        }
    }])
    with pytest.raises(ValidationError):
        validator.validate([{'url': 'http://rero.ch/files/test.pdf'}])


def test_from_marc():
    record = marc2record({
        '300__': {
            'a': '100 p.',
            'b': 'ill.',
            'c': '25 x 30 cm'
        },
        '8564_': [{
            'f': 'file_name.pdf',
            'q': 'application/pdf',
            's': '1014',
            'u': 'http://doc.rero.ch/record/file_name.pdf',
            'y': 'order:1',
            'z': 'Main file'
        }]
    })

    assert record == {
        'document': [{
            'name': 'file_name.pdf',
            'mime': 'application/pdf',
            'size': 1014,
            'url': 'http://doc.rero.ch/record/file_name.pdf',
            'label': 'Main file',
            'physical_description': {
                'extent': '100 p.',
                'details': 'ill.',
                'dimensions': '25 x 30 cm'
            }
        }]
    }


def test_marc2marc():
    marc = {
        '300__': {
            'a': '100 p.',
            'b': 'ill.',
            'c': '25 x 30 cm'
        },
        '8564_': [{
            'f': 'file_name.pdf',
            'q': 'application/pdf',
            's': '1014',
            'u': 'http://doc.rero.ch/record/file_name.pdf',
            'y': 'order:1',
            'z': 'Main file'
        }]
    }
    converted = marc2marc(marc)
    assert marc == converted


def test_multiple_marc2marc():
    marc = {
        '8564_': [{
            'f': 'digs_complete_postprint_v1.pdf',
            'q': 'application/pdf',
            's': '2086891',
            'u': 'http://doc.rero.ch/record/8488/files/' +
                 'digs_complete_postprint_v1.pdf',
            'y': 'order:1',
            'z': 'Texte intégral'
        }, {
            'f': 'digs_cover_front.pdf',
            'q': 'application/pdf',
            's': '2605703',
            'u': 'http://doc.rero.ch/record/8488/files/digs_cover_front.pdf',
            'y': 'order:2',
            'z': 'Couverture avant'
        }, {
            'f': 'digs_cover_rear.pdf',
            'q': 'application/pdf',
            's': '192617',
            'u': 'http://doc.rero.ch/record/8488/files/digs_cover_rear.pdf',
            'y': 'order:3',
            'z': 'Couverture arrière'
        }, {
            'f': 'digs_complete_abstract.pdf',
            'q': 'application/pdf',
            's': '6361',
            'u': 'http://doc.rero.ch/record/8488/files/digs_complete_abs.pdf',
            'y': 'order:4',
            'z': 'Résumé'
        }]
    }
    converted = marc2marc(marc)
    assert marc == converted


def test_multiple_sort_marc2marc():
    bad_sorted_marc = {
        '8564_': [{
            'f': 'digs_complete_abstract.pdf',
            'q': 'application/pdf',
            's': '6361',
            'u': 'http://doc.rero.ch/record/8488/files/digs_complete_abs.pdf',
            'y': 'order:4',
            'z': 'Résumé'
        }, {
            'f': 'digs_complete_postprint_v1.pdf',
            'q': 'application/pdf',
            's': '2086891',
            'u': 'http://doc.rero.ch/record/8488/files/' +
                 'digs_complete_postprint_v1.pdf',
            'y': 'order:1',
            'z': 'Texte intégral'
        }, {
            'f': 'digs_cover_front.pdf',
            'q': 'application/pdf',
            's': '2605703',
            'u': 'http://doc.rero.ch/record/8488/files/digs_cover_front.pdf',
            'y': 'order:2',
            'z': 'Couverture avant'
        }, {
            'f': 'digs_cover_rear.pdf',
            'q': 'application/pdf',
            's': '192617',
            'u': 'http://doc.rero.ch/record/8488/files/digs_cover_rear.pdf',
            'y': 'order:3',
            'z': 'Couverture arrière'
        }]
    }
    marc = {
        '8564_': [{
            'f': 'digs_complete_postprint_v1.pdf',
            'q': 'application/pdf',
            's': '2086891',
            'u': 'http://doc.rero.ch/record/8488/files/' +
                 'digs_complete_postprint_v1.pdf',
            'y': 'order:1',
            'z': 'Texte intégral'
        }, {
            'f': 'digs_cover_front.pdf',
            'q': 'application/pdf',
            's': '2605703',
            'u': 'http://doc.rero.ch/record/8488/files/digs_cover_front.pdf',
            'y': 'order:2',
            'z': 'Couverture avant'
        }, {
            'f': 'digs_cover_rear.pdf',
            'q': 'application/pdf',
            's': '192617',
            'u': 'http://doc.rero.ch/record/8488/files/digs_cover_rear.pdf',
            'y': 'order:3',
            'z': 'Couverture arrière'
        }, {
            'f': 'digs_complete_abstract.pdf',
            'q': 'application/pdf',
            's': '6361',
            'u': 'http://doc.rero.ch/record/8488/files/digs_complete_abs.pdf',
            'y': 'order:4',
            'z': 'Résumé'
        }]
    }
    converted = marc2marc(bad_sorted_marc)
    assert marc == converted
