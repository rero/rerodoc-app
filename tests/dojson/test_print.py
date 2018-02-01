# -*- coding: utf-8 -*-
import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator

validator = validator('common/print-0.0.1.json')
assert validator


def test_validate_record():
    validator.validate({
            'location': 'Geneva',
            'printer': 'Imprimeurs de Genève'
    })


def test_from_marc():
    record = marc2record({
        '260__': {
            'a': 'Location',
            'b': 'Publisher',
            'c': '2015-2017',
            'e': 'Print Location',
            'f': 'Printer'
        }
    })
    assert record.get('print') == {
        'location': 'Print Location',
        'printer': 'Printer'
    }
