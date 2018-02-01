"""MARC 21 model definition."""

import re

from dojson import utils
from isbnlib import ean13

from ..models import book, book2marc


@book.over('isbn', '^020..')
@utils.ignore_value
def isbn(self, key, value):
    """Other Standard Identifier."""
    isbn = value.get('a')
    ean = ean13(isbn) or isbn
    return ean


@book2marc.over('020__', 'isbn')
def isbn2marc(self, key, value):
    """Other Standard Identifier."""
    return {
        'a': value
    }
