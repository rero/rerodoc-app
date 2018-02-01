"""MARC 21 model definition."""

from dojson import utils

from .. import utils as myutils
from ..models import audio, audio2marc


@audio.over('publication', '^260__')
@utils.filter_values
def publication(self, key, value):
    """Publication Statement."""
    return {
        'location': value.get('a'),
        'publisher': value.get('b'),
        'date': value.get('c'),
        'full': myutils.concatenate(value, ['a', 'b', 'c'])
    }


@audio2marc.over('260__', '^publication$')
@utils.filter_values
def publication2marc(self, key, value):
    """Edition Statement."""
    return {
        'a': value.get('location'),
        'b': value.get('publisher'),
        'c': value.get('date')
    }
