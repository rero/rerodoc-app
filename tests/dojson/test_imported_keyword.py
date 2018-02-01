import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator
from jsonschema import ValidationError

validator = validator('common/imported_keyword-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate([{
        'language': 'fr',
        'vocabulary': 'rero',
        'value': ['keyword1', 'keyword2']
    }])


def test_from_marc():
    record = marc2record({
        '600__': [{
            '2': 'rero',
            '9': '650_7',
            'a': 'crime organisé -- drogue - trafic'
                 ' -- sécurité nationale -- Amérique du sud'
        }]
    })
    assert record == {
        'imported_keyword': [{
            'language': 'fr',
            'vocabulary': 'rero',
            'value': [
                'crime organisé',
                'drogue - trafic',
                'sécurité nationale',
                'Amérique du sud'
            ]
        }]
    }


def test_mesh_from_marc():
    record = marc2record({
        '600__': [{
            '9': '650_2',
            'a': 'Inventaires'
        }]
    })
    assert record == {
        'imported_keyword': [{
            'vocabulary': 'mesh',
            'language': 'fr',
            'value': ['Inventaires']
        }]
    }


def test_lcsh_from_marc():
    record = marc2record({
        '600__': [{
            '9': '650__',
            'a': 'Inventaires'
        }]
    })
    assert record == {
        'imported_keyword': [{
            'vocabulary': 'lcsh',
            'language': 'fr',
            'value': ['Inventaires']
        }]
    }


def test_marc2marc():
    marc = {
        '600__': [{
            '2': 'rero',
            'a': 'crime organisé -- drogue - trafic '
                 '-- sécurité nationale -- Amérique du sud'
        }]
    }
    converted = marc2marc(marc)
    assert marc == converted
