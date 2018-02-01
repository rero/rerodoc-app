# -*- coding: utf-8 -*-

import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator
from jsonschema import ValidationError

validator = validator('common/access_restriction-0.0.1.json')
assert validator


def test_validate_record():
    assert validator
    validator.validate('Restricted access')
    validator.validate('free')
    validator.validate('No access until 2015-01-01')
    with pytest.raises(ValidationError):
        validator.validate('No access until 2015')


def test_from_marc():
    record = marc2record({
        '506__': {
            'a': u'Accès réservé aux institutions membres de RERO',
            'f': 'Restricted access',
        }
    })
    assert record.get('access_restriction') == 'Restricted access'


def test_marc2marc():
    marc = {
        '506__': {
            'a': u'Accès réservé aux institutions membres de RERO',
            'f': 'Restricted access',
        }
    }
    converted = marc2marc(marc)
    assert marc == converted
