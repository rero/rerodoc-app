import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator
from jsonschema import ValidationError

validator = validator('common/institution-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate(
        'hevs'
    )
    with pytest.raises(ValidationError):
        validator.validate('HEVS_')


def test_from_marc():
    record = marc2record({
        '980__': {
            'a': 'BOOK',
            'b': 'MEDVS'
        }
    })
    assert record.get('institution') == 'medvs'


def test_marc2marc():
    marc = {
        '980__': {
            'a': 'BOOK',
            'b': 'MEDVS'
        }
    }

    converted = marc2marc(marc)
    assert marc == converted
