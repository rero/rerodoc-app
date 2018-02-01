# -*- coding: utf-8 -*-

"""MARC 21 model definition."""

import copy
import re

from dojson import Overdo, utils

from . import utils as myutils
from .utils import lang2ln, ln2lang

book = Overdo()
book2marc = Overdo()


class BadDateFormatException(Exception):
    """Bad date format custom Exception."""

    pass


def get_number_of_pages(value):
    """Retrive number of pages in a given string."""
    raw_pages = value.get('a')
    if not raw_pages:
        return None

    n_pages = re.findall(r'(\d+)\s*(?:p|s|f)', raw_pages, re.IGNORECASE)
    if n_pages:
        return int(n_pages[0])
    else:
        n_pages = re.findall(r'^(\d+)$', raw_pages)
        if n_pages:
            return int(n_pages[0])
    return None


def extract_date(date):
    """Extract a date ising regular expression."""
    if not date:
        return None, None
    from_date = None
    to_date = None

    # year only
    regex = re.match(r'^(\w{4})-{0,1}$', date)
    if regex:
        from_date = regex.group(1)

    regex = re.match(r'^(\w{4})-(\w{4})$', date)
    if regex:
        from_date = regex.group(1)
        to_date = regex.group(2)
    # year-month-day
    regex = re.match(r'^(\w{4}-\w{1,2}-\w{1,2})-{0,1}$', date)
    if regex:
        from_date = regex.group(1)
    if not from_date:
        res = re.findall(r'(\w{4})', date)
        if len(res) == 1:
            from_date = res[0]
        if len(res) == 2:
            from_date, to_date = res
    return from_date, to_date


@book.over('recid', '^001')
def control_number(self, key, value):
    """Record Identifier."""
    return value


@book2marc.over('001', 'recid')
def control_number2marc(self, key, value):
    """Record Identifier."""
    return value


@book.over('reroid', '^035__')
def reroid(self, key, value):
    """Language Code."""
    return "http://data.rero.ch/01-" + value.get('a')


@book2marc.over('035__', 'reroid')
def reroid2marc(self, key, value):
    """Language Code."""
    return {
        'a': value.replace("http://data.rero.ch/01-", "")
    }


@book.over('language', '^041[10_].')
def language(self, key, value):
    """Language Code."""
    return lang2ln(value.get('a'))


@book2marc.over('041__', 'language')
def language2marc(self, key, value):
    """Language Code."""
    return {
        'a': ln2lang(value)
    }


@book.over('udc', '^080__')
@utils.ignore_value
def udc(self, key, value):
    """Language Code."""
    return value.get('a')


@book2marc.over('080__', 'udc')
@utils.ignore_value
def udc2marc(self, key, value):
    """Language Code."""
    return {
        'a': value
    }


@book.over('contributor', '^(10|70|71)0__')
def contributor(self, key, value):
    """Record Document Type."""
    value = utils.force_list(value)
    contributors = self.get('contributor', [])

    def get_value(value):
        date = value.get("d")

        birthdate, deathdate = extract_date(date)
        map_roles = {
            'Dir.': 'thesis director',
            'Codir.': 'thesis codirector',
            'Libr./Impr.': 'editor'
        }
        to_return = {
            "name": value.get("a"),
            "role": map_roles.get(value.get("e"), 'author'),
            "type": "person",
            "affiliation": value.get("u")
        }
        if birthdate:
            to_return['birth_date'] = birthdate
        if deathdate:
            to_return['death_date'] = deathdate
        return dict((k, v) for k, v in to_return.items() if v)

    if key.startswith('100'):
        contributors.insert(0, get_value(value[0]))

    elif key.startswith('710'):
        for val in value:
            tmp = {
                'name': val.get('a'),
                'type': 'corporate',
                'role': 'author'
            }
            contributors.append(tmp)
    else:
        c = []
        for val in value:
            c.append(get_value(val))
        if contributors and contributors[0]['type'] == 'corporate':
            contributors = c + contributors
        elif len(contributors) > 1 and contributors[0]['type'] == 'person':
            contributors = [contributors[0]] + c + contributors[1:]
        else:
            contributors = contributors + c
    return contributors


@book2marc.over('100__', 'contributor')
# @utils.filter_values
def authors2marc(self, key, value):
    """Main Entry-Personal Name."""
    value = utils.force_list(value)

    def get_value(value):
        map_roles = {
            'thesis director': 'Dir.',
            'thesis codirector': 'Codir.',
            'editor': 'Libr./Impr.'
        }
        to_return = {
            'a': value.get('name'),
            'e': map_roles.get(value.get('role')),
            'd': '-'.join((value.get('birth_date', ''),
                           value.get('death_date', ''))),
            'u': value.get('affiliation')
        }
        return dict((k, v) for k, v in to_return.items() if v)

    first_author = None
    if value[0].get('type') == 'person':
        first_author = get_value(value[0])

    for author in value[1:]:
        if author.get('type') == 'person':
            self.setdefault('700__', []).append(get_value(author))
        else:
            self.setdefault('710__', []).append({
                'a': author.get('name')
            })

    return first_author


@book.over('title', '^245__')
@utils.for_each_value
@utils.filter_values
def title(self, key, value):
    """Other title Statement."""
    return {
        'main': value.get('a'),
        'sub': value.get('b'),
        'language': lang2ln(value.get('9'))
    }


@book2marc.over('245__', 'title')
@utils.for_each_value
@utils.filter_values
def title2marc(self, key, value):
    """Title Statement."""
    return {
        'a': value.get('main'),
        'b': value.get('sub'),
        '9': ln2lang(value.get('language'))
    }


@book.over('other_title', '^246__')
@utils.for_each_value
@utils.filter_values
def other_title(self, key, value):
    """Other title Statement."""
    return {
        'main': value.get('a'),
        'sub': value.get('b'),
        'language': lang2ln(value.get('9')) or 'fr'
    }


@book2marc.over('246__', 'other_title')
@utils.for_each_value
@utils.filter_values
def other_title2marc(self, key, value):
    """Title Statement."""
    return {
        'a': value.get('main'),
        'b': value.get('sub'),
        '9': ln2lang(value.get('language'))
    }


@book.over('edition', '^250__')
@utils.filter_values
def edition(self, key, value):
    """Edition Statement."""
    return {
        'statement': value.get('a'),
        'remainder': value.get('b')
    }


@book2marc.over('250__', 'edition')
@utils.filter_values
def edition2marc(self, key, value):
    """Edition Statement."""
    return {
        'a': value.get('statement'),
        'b': value.get('remainder')
    }


@book.over('publication', '^260__')
@utils.filter_values
def publication(self, key, value):
    """Publication Statement."""
    _print = {}
    if value.get('e'):
        _print['location'] = value.get('e')
    if value.get('f'):
        _print['printer'] = value.get('f')
    if _print:
        self['print'] = _print
    start_date, end_date = extract_date(value.get('c'))

    return {
        'location': value.get('a'),
        'publisher': value.get('b'),
        'date_label': value.get('c'),
        'start_date': start_date,
        'end_date': end_date,
    }


@book2marc.over('260__', '^publication$')
@utils.filter_values
def publication2marc(self, key, value):
    """Edition Statement."""
    publication_statement = self.get('260__', {})
    publication_statement.update({
        'a': value.get('location'),
        'b': value.get('publisher'),
        'c': value.get('date_label')
    })
    return publication_statement


@book2marc.over('260__', '^print$')
@utils.filter_values
def print2marc(self, key, value):
    """Edition Statement."""
    publication_statement = self.get('260__', {})
    publication_statement.update({
        'f': value.get('printer'),
        'e': value.get('location')
    })
    return publication_statement


@book.over('series', '^490__')
@utils.filter_values
def series(self, key, value):
    """Series Statement."""
    return {
        'name': value.get('a'),
        'volume': value.get('v')
    }


@book2marc.over('490__', 'series')
@utils.filter_values
def series2marc(self, key, value):
    """Collation Statement."""
    return {
        'a': value.get('name'),
        'v': value.get('volume')
    }


@book.over('note', '^500__')
@utils.for_each_value
def note(self, key, value):
    """Note Statement."""
    return value.get('a')


@book2marc.over('500__', 'note')
@utils.for_each_value
def note2marc(self, key, value):
    """Note Statement."""
    return {
        'a': value
    }


@book.over('content_note', '^505__')
@utils.for_each_value
def content_note(self, key, value):
    """Content Note Statement."""
    return value.get('a')


@book2marc.over('505__', 'content_note')
@utils.for_each_value
def content_note2marc(self, key, value):
    """Content Note Statement."""
    return {
        'a': value
    }


@book.over('access_restriction', '^506__')
# @utils.filter_values
def access_restriction(self, key, value):
    """Content Note Statement."""
    return value.get('f')


@book2marc.over('506__', 'access_restriction')
@utils.filter_values
def access_restriction2marc(self, key, value):
    """Content Note Statement."""
    return {
        'a': 'Accès réservé aux institutions membres de RERO',
        'f': value
    }


@book.over('summary', '^520__')
@utils.for_each_value
def summary(self, key, value):
    """Summary Statement."""
    return {
        'value': value.get('a'),
        'language': lang2ln(value.get('9'))
    }


@book2marc.over('520__', 'summary')
@utils.for_each_value
def summary2marc(self, key, value):
    """Summary Statement."""
    return {
        'a': value.get('value'),
        '9': ln2lang(value.get('language'))
    }


@book.over('digitization', '^533__')
@utils.filter_values
def digitization(self, key, value):
    """Reproduction Statement."""
    return {
        'location': value.get('b'),
        'digitizer': value.get('c'),
        'date': value.get('d')
    }


@book2marc.over('533__', 'digitization')
@utils.filter_values
def digitization2marc(self, key, value):
    """Summary Statement."""
    return {
        'a': 'Electronic reproduction',
        'b': value.get('location'),
        'c': value.get('digitizer'),
        'd': value.get('date')
    }


@book.over('imported_keyword', '^600__')
@utils.for_each_value
def subject(self, key, value):
    """Subject Statement."""
    to_return = {
        'language': 'fr',
        'value': value.get('a').split(' -- ')
    }
    vocabulary = value.get('2')
    if not vocabulary:
        ind = value.get('9')[-1]
        if ind == '2':
            vocabulary = 'mesh'
        elif ind == '_':
            vocabulary = 'lcsh'

    if vocabulary:
        to_return['vocabulary'] = vocabulary

    return to_return


@book2marc.over('600__', 'imported_keyword')
@utils.for_each_value
def subject2marc(self, key, value):
    """Subject Statement."""
    return {
        '2': value.get('vocabulary'),
        'a': ' -- '.join(value.get('value'))
    }


@book.over('keyword', '^695__')
@utils.for_each_value
def keyword(self, key, value):
    """Keyword Statement."""
    keywords = [v.strip() for v in value.get('a').split(';')]
    return {
        'language': lang2ln(value.get('9')),
        'value': [v for v in keywords if v]
    }


@book2marc.over('695__', 'keyword')
@utils.for_each_value
def subject2marc(self, key, value):
    """Subject Statement."""
    return {
        '9': ln2lang(value.get('language')),
        'a': " ; ".join(value.get('value'))
    }


@book.over('meeting', '^711__')
@utils.filter_values
def meeting(self, key, value):
    """Meeting Statement."""
    return {
        'name': value.get('a'),
        'location': value.get('c'),
        'date': value.get('d'),
        'number': value.get('n')
    }


@book2marc.over('711__', 'meeting')
@utils.filter_values
def meeting2marc(self, key, value):
    """Meeting Statement."""
    return {
        "a": value.get("name"),
        "c": value.get("location"),
        "d": value.get("date"),
        "n": value.get("number")
    }


@book.over('other_edition', '^775__')
@utils.for_each_value
def other_edition(self, key, value):
    """Other Edition Statement."""
    url = value.get('o', '')
    if not url.startswith('http') and value.get('g', '').startswith('http'):
        url = value.get('g')
    return {
        'type': 'published version',
        'url': url
    }


@book2marc.over('775__', 'other_edition')
@utils.for_each_value
def other_edition2marc(self, key, value):
    """Other Edition Statement."""
    return {
        'g': value.get('type'),
        'o': value.get('url')
    }


@book.over('document', '^8564_|^300__')
@utils.ignore_value
def document(self, key, value):
    """Document Statement."""
    document = self.get('document', [])
    links = self.get('external_link', [])
    physical_description = self.get('_physical_description')

    def add_physical_in_document(physical_description, documents):
        doc = documents[0]
        pd = physical_description
        doc.setdefault('physical_description', {})
        if pd.get('a'):
            doc['physical_description']['extent'] = pd.get('a')
        if pd.get('b'):
            doc['physical_description']['details'] = pd.get('b')
        if pd.get('c'):
            doc['physical_description']['dimensions'] = pd.get('c')

    if key.startswith('300__'):
        self['_physical_description'] = value
        physical_description = value
    else:
        value = utils.force_list(value)

        def get_doc_value(value):
            return {
                'name': value.get('f'),
                'mime': value.get('q'),
                'size': int(value.get('s')),
                'url': value.get('u'),
                'label': value.get('z')
            }

        def get_link_value(value):
            return {
                'url': value.get('u'),
                'label': value.get('z')
            }

        for val in value:
            if not val.get('q'):
                links.append(get_link_value(val))
        if links:
            self['external_link'] = links

        def sort_order(x):
            value = x.get('y', '')
            if value.startswith('order:'):
                return int(value.replace('order:', ''))
            return 0
        for val in sorted(value,
                          key=sort_order):
            if val.get('q'):
                document.append(get_doc_value(val))

    if physical_description and document:
        add_physical_in_document(physical_description, document)
        del(self['_physical_description'])

    return document or None


@book2marc.over('8564_', '(^document$|external_link)')
def document2marc(self, key, value):
    """Document Statement."""
    value = utils.force_list(value)
    f8564 = self.get('8564_', [])
    links = []
    document = []
    if key.startswith('external_link'):
        def get_value(value):
            return {
                'u': value.get('url'),
                'z': value.get('label')
            }
        for val in value:
            links.append(get_value(val))
        return links + f8564
    else:
        def get_value(value, order):
            pd = value.get('physical_description')
            if pd:
                to_add = {}
                if pd.get('extent'):
                    to_add['a'] = pd.get('extent')
                if pd.get('details'):
                    to_add['b'] = pd.get('details')
                if pd.get('dimensions'):
                    to_add['c'] = pd.get('dimensions')
                self['300__'] = to_add

            return {
                'f': value.get('name'),
                'q': value.get('mime'),
                's': str(value.get('size')),
                'u': value.get('url'),
                'y': "order:%s" % order,
                'z': value.get('label')
            }
        for order, val in enumerate(value):
            document.append(get_value(val, order+1))
        return f8564 + document
    return f8564


@book.over('institution', '^980__')
def institution(self, key, value):
    """Institution Statement."""
    self['type'] = {
        'main': value.get('a').lower()
    }
    if value.get('f'):
        self['type']['sub'] = value.get('f').lower()

    return value.get('b').lower().replace('_', '')


@book2marc.over('980__', 'institution')
@utils.filter_values
def insitution2marc(self, key, value):
    """Record Document Type and Institution."""
    marc = self.get('980__', {})
    marc.update({
        'b': value.upper()
    })
    return marc


@book2marc.over('980__', 'type')
@utils.filter_values
def type2marc(self, key, value):
    """Record Document Type and Institution."""
    marc = self.get('980__', {})
    sub = value.get('sub')
    if sub:
        sub = sub.upper()
    marc.update({
        'a': value.get('main').upper(),
        'f': sub
        })
    return marc


@book.over('specific_collection', '^982__')
@utils.for_each_value
@utils.ignore_value
def specific_collection(self, key, value):
    """Specific Collection Statement."""
    name = []
    if value.get('a'):
        name.append(value.get('a'))
    if value.get('b'):
        name.append(value.get('b'))
    return ';'.join(name)


@book2marc.over('982__', 'specific_collection')
@utils.for_each_value
@utils.filter_values
def series2marc(self, key, value):
    """Specific Collection Statement."""
    return {
        'a': value
    }


audio = copy.deepcopy(book)
audio2marc = copy.deepcopy(book2marc)

report = copy.deepcopy(book)
report2marc = copy.deepcopy(book2marc)
