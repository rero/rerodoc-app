import pytest
from conftest import marc2marc, marc2record, record2jsonld, validator
from jsonschema import ValidationError

validator = validator('common/contributor-0.0.1.json')
assert validator


def test_validate_record():
    record = [{
            'name': 'LastName, FirstName',
            'birth_date': '1971',
            'death_date': '2001',
            'role': 'thesis director',
            'affiliation': 'Affiliation',
            'orcid': 'http://orcid.org/0000-0001-8368-5460',
            'type': 'person'
        }, {
            'name': 'Corporate',
            'role': 'editor',
            'type': 'corporate'
        }]
    validator.validate(record)
    with pytest.raises(ValidationError):
        validator.validate([{'role': 'foo'}])
    with pytest.raises(ValidationError):
        validator.validate([{'orcid': '0000-0001-8368-5460'}])


def test_first_author_from_marc():
    record = marc2record({
        '100__': {
            'a': 'LastName, FirstName',
            'd': '1971-',
            'e': 'Dir.',
            'u': 'Affiliation'
        }
    })
    assert record == {
        'contributor': [{
            'name': 'LastName, FirstName',
            'birth_date': '1971',
            'role': 'thesis director',
            'type': 'person',
            'affiliation': 'Affiliation'
        }]
    }


def test_first_author_marc2marc():
    marc = {
        '100__': {
            'a': 'LastName, FirstName',
            'd': '1971-',
            'e': 'Dir.',
            'u': 'Affiliation'
        }
    }
    converted = marc2marc(marc)
    assert marc == converted


def test_multiple_authors_from_marc():
    record = marc2record({
        '100__': {
            'a': 'LastName, FirstName',
            'd': '1971-',
            'u': 'Affiliation'
        },
        '700__': [{
            'a': 'LastName2, FirstName2',
            'd': '1941-1978',
            'e': 'join author',
            'u': 'Affiliation2'
        }, {
            'a': 'LastName3, FirstName3',
            'd': '1974-01-01',
            'e': 'Codir.',
            'u': 'Affiliation'
        }, {
            'a': 'LastName4, FirstName4',
            'd': '1974',
            'e': 'Libr./Impr.'
        }],
        '710__': [{
            'a': 'Name1',
        }, {
            'a': 'Name2'
        }]
    })
    assert record == {
        'contributor': [{
            'name': 'LastName, FirstName',
            'birth_date': '1971',
            'affiliation': 'Affiliation',
            'type': 'person',
            'role': 'author'
        }, {
            'name': 'LastName2, FirstName2',
            'birth_date': '1941',
            'death_date': '1978',
            'role': 'theis director',
            'affiliation': 'Affiliation2',
            'type': 'person',
            'role': 'author'
        }, {
            'name': 'LastName3, FirstName3',
            'birth_date': '1974-01-01',
            'affiliation': 'Affiliation',
            'role': 'thesis codirector',
            'type': 'person'
        }, {
            'name': 'LastName4, FirstName4',
            'birth_date': '1974',
            'role': 'editor',
            'type': 'person'
        }, {
            'name': 'Name1',
            'type': 'corporate',
            'role': 'author'
        }, {
            'name': 'Name2',
            'type': 'corporate',
            'role': 'author'
        }]
    }


def test_multiple_authors_marc2marc():
    marc = {
        '100__': {
            'a': 'LastName, FirstName',
            'd': '1971-',
            'u': 'Affiliation'
        },
        '700__': [{
            'a': 'LastName2, FirstName2',
            'd': '1941-1978',
            'u': 'Affiliation2'
        }, {
            'a': 'LastName3, FirstName3',
            'd': '1974-01-01-',
            'e': 'Codir.',
            'u': 'Affiliation'
        }, {
            'a': 'LastName4, FirstName4',
            'd': '1974-',
            'e': 'Libr./Impr.'
        }],
        '710__': [{
            'a': 'Name1',
        }, {
            'a': 'Name2'
        }]
    }
    converted = marc2marc(marc)
    assert marc == converted


def test_first_author_jsonld(book_context):
    record = {
        'recid': '1234',
        'contributor': [{
            'name': 'LastName, FirstName',
            'date': '1971-',
            'role': 'Dir.',
            'affilation': 'Affiliation',
            'full': 'LastName, FirstName 1971-'
        }]
    }
    converted = record2jsonld(record, book_context)
    jsonld = [{
        '@id': 'http://doc.rero.ch/record/1234',
        'http://purl.org/dc/elements/1.1/creator': [{
            '@value': 'LastName, FirstName 1971-'
        }]
    }]
    assert converted == jsonld
