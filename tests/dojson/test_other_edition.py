import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator
from jsonschema import ValidationError

validator = validator('common/other_edition-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate([{
        'type': 'published version',
        'url': 'http://dx.doi.org/10.1111/j.1365-3032.2012.00840.x'
    }])
    validator.validate([{
        'type': 'published version',
        'url': 'https://dx.doi.org/10.1111/j.1365-3032.2012.00840.x'
    }])
    with pytest.raises(ValidationError):
        validator.validate([{'url': 'bla'}])


def test_from_marc():
    record = marc2record({
        '775__': {
            'g': 'published version',
            'o': 'http://dx.doi.org/10.1111/j.1365-3032.2012.00840.x'
        }
    })
    assert record == {
        'other_edition': [{
            'type': 'published version',
            'url': 'http://dx.doi.org/10.1111/j.1365-3032.2012.00840.x'
        }]
    }


def test_marc2marc():
    marc = {
        '775__': [{
            'g': 'published version',
            'o': 'http://dx.doi.org/10.1111/j.1365-3032.2012.00840.x'
        }]
    }
    converted = marc2marc(marc)
    assert marc == converted
