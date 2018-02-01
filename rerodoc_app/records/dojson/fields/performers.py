"""MARC 21 model definition."""

from dojson import utils

from ..models import audio, audio2marc


@audio.over('performers', '^511__')
@utils.ignore_value
def performers(self, key, value):
    """Performers List."""
    return value.get('a')


@audio2marc.over('511__', 'performers')
def isbn102marc(self, key, value):
    """Perfomers List."""
    return {
        'a': value
    }
