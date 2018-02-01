
from rerodoc_app.views import format_metadata


def test_title():
    assert format_metadata(
        'title',
        {
            'title': [{
                'main': '<maintitle>',
                'sub': '<subtitle>',
                'language': 'en'
            }]
        }
    ) == [{
        'label': 'title_en',
        'value': ['<maintitle> : <subtitle>']
    }]

    assert format_metadata(
        'title',
        {
            'title': [{
                'main': '<maintitle>',
                'language': 'en'
            }]
        }
    ) == [{
        'label': 'title_en',
        'value': ['<maintitle>']
    }]

    assert format_metadata(
        'title',
        {
            'title': [{
                'main': '<main_title_1>',
                'sub': '<subtitle_1>',
                'language': '<language_1>'
            }, {
                'main': '<maintitle_2>',
                'language': '<language_2>'
            }]
        }
    ) == [{
        'label': 'title_<language_1>',
        'value': ['<main_title_1> : <subtitle_1>']
    }, {
        'label': 'title_<language_2>',
        'value': ['<maintitle_2>']
    }]


def test_other_title():
    assert format_metadata(
        'other_title',
        {
            'other_title': [{
                'main': '<maintitle>',
                'sub': '<subtitle>',
                'language': 'en'
            }]
        }
    ) == [{
        'label': 'other_title_en',
        'value': ['<maintitle> : <subtitle>']
    }]

    assert format_metadata(
        'other_title',
        {
            'other_title': [{
                'main': '<maintitle>',
                'language': 'en'
            }]
        }
    ) == [{
        'label': 'other_title_en',
        'value': ['<maintitle>']
    }]

    assert format_metadata(
        'other_title',
        {
            'other_title': [{
                'main': '<titre_principal>',
                'sub': '<titre_secondaire>',
                'language': '<language_1>'
            }, {
                'main': '<maintitle>',
                'language': '<language_2>'
            }]
        }
    ) == [{
        'label': 'other_title_<language_1>',
        'value': ['<titre_principal> : <titre_secondaire>']
    }, {
        'label': 'other_title_<language_2>',
        'value': ['<maintitle>']
    }]


def test_authors(contributor):
    assert format_metadata('author', contributor) == [{
        'label': 'author',
        'value': [
            '<lastname1>, <fistname1>, 1971 (<affiliation1>). '
            'http://orcid.org/0000-0001-8368-5460',
            '<name1>.',
            '<name2>.'
        ]
    }]


def test_scientific_editor(contributor):
    assert format_metadata('editor', contributor) == [{
        'label': 'editor',
        'value': [
            '<lastname4>, <fistname4>, 1974.'
        ]
    }]


def test_thesis_director(contributor):
    assert format_metadata('thesis director', contributor) == [{
        'label': 'thesis director',
        'value': [
            '<lastname2>, <fistname2>, 1941-1978 (<affiliation2>).'
        ]
    }]


def test_thesis_codirector(contributor):
    assert format_metadata('thesis codirector', contributor) == [{
        'label': 'thesis codirector',
        'value': [
            '<lastname3>, <fistname3>, 1974 (<affiliation3>).'
        ]
    }]


def test_printer(contributor):
    assert format_metadata('printer', contributor) == [{
        'label': 'printer',
        'value': [
            '<name3>.'
        ]
    }]


def test_language():
    assert format_metadata('language', {'language': 'en'}) == [{
        'label': 'language',
        'value': [
            'en'
        ]
    }]


def test_edition():
    assert format_metadata('edition', {
        'edition': {
            'statement': '<statement>',
            'remainder': '<remainder>'
        }
    }) == [{
        'label': 'edition',
        'value': [
            '<statement> / <remainder>'
        ]
    }]


def test_publication():
    assert format_metadata('publication', {
        'publication': {
            'publisher': '<publisher>',
            'location': '<location>',
            'date_label': '<date_label>'
        }
    }) == [{
        'label': 'publication',
        'value': [
            '<location> : <publisher>, <date_label>'
        ]
    }]


def test_print():
    assert format_metadata('print', {
        'print': {
            'printer': '<printer>',
            'location': '<location>'
        }
    }) == [{
        'label': 'print',
        'value': [
            '<location> : <printer>'
        ]
    }]


def test_collation():
    assert format_metadata('collation', {
        'document': [{
            'physical_description': {
                'extent': '<extent1>',
                'details': '<details1>',
                'dimensions': '<dimensions1>'
            }
        }, {
            'physical_description': {
                'extent': '<extent2>',
                'details': '<details2>',
                'dimensions': '<dimensions2>'
            }
        }]
    }) == [{
        'label': 'collation',
        'value': [
            '<extent1> : <details1>, <dimensions1>',
            '<extent2> : <details2>, <dimensions2>'
        ]
    }]


def test_series():
    assert format_metadata('series', {
        'series': {
            'name': '<name>',
            'volume': '<volume>'
        }
    }) == [{
        'label': 'series',
        'value': [
            '<name> ; <volume>'
        ]
    }]


def test_imported_keyword():
    assert format_metadata('imported_keyword', {
        'imported_keyword': [{
            'value': ['<keyword1>', '<keyword2>'],
            'language': 'en',
            'vocabulary': 'rero'
        }, {
            'value': ['<keyword3>', '<keyword4>', '<keyword5>'],
            'language': 'en',
            'vocabulary': 'jurivoc'
        }]
    }) == [{
        'label': 'imported_keyword_rero',
        'value': ['<keyword1> - <keyword2>']
    }, {
        'label': 'imported_keyword_jurivoc',
        'value': ['<keyword3> - <keyword4> - <keyword5>']
    }]


def test_keyword():
    assert format_metadata('keyword', {
        'keyword': [{
            'value': ['<keyword1>', '<keyword2>'],
            'language': 'en'
        }, {
            'value': ['<keyword3>', '<keyword4>', '<keyword5>'],
            'language': 'fr'
        }]
    }) == [{
        'label': 'keyword',
        'value': [
            '<keyword1> ; <keyword2>',
            '<keyword3> ; <keyword4> ; <keyword5>'
        ]
    }]


def test_udc():
    assert format_metadata('udc', {'udc': '78'}, 'fr') == [{
        'label': 'udc',
        'value': [
            'Musique'
        ]
    }]


def test_meeting():
    assert format_metadata('meeting', {
        'meeting': {
            'name': '<name>',
            'location': '<location>',
            'date': '<date>',
            'number': '<number>'
        }
    }) == [{
        'label': 'meeting',
        'value': [
            '<name> (<number> : <date> : <location>)'
        ]
    }]


def test_content_note():
    assert format_metadata('content_note', {
        'content_note': [
            '<note1>'
            '<note2>'
            '<note3>'
            ]
    }) == [{
        'label': 'content_note',
        'value': [
            '<note1>'
            '<note2>'
            '<note3>'
        ]
    }]


def test_note():
    assert format_metadata('note', {
        'note': [
            '<note1>'
            '<note2>'
            '<note3>'
            ]
    }) == [{
        'label': 'note',
        'value': [
            '<note1>'
            '<note2>'
            '<note3>'
        ]
    }]


def test_other_edition():
    # TODO: label translation
    assert format_metadata('other_edition', {
        'other_edition': [{
            'type': 'published version',
            'url': 'http://dx.doi.org/10.1111/j.1365-3032.2012.00840.x'
        }]
    }) == [{
        'label': 'other_edition',
        'value': [
            '<a href="http://dx.doi.org/10.1111/j.1365-3032.2012.00840.x">'
            'published version'
            '</a>'
            ]
    }]


def test_external_link():
    # TODO: label translation
    assert format_metadata('external_link', {
        'external_link': [{
            'label': 'Web site',
            'url': 'http://web.site.com'
        }]
    }) == [{
        'label': 'external_link',
        'value': [
            '<a href="http://web.site.com">'
            'Web site'
            '</a>'
            ]
    }]


def test_digitization():
    assert format_metadata('digitization', {
        'digitization': {
            'digitizer': '<digitizer>',
            'location': '<location>',
            'date': '<date>'
        }
    }) == [{
        'label': 'digitization',
        'value': [
            '<location> : <digitizer>, <date>'
        ]
    }]


def test_isbn():
    assert format_metadata('isbn', {'isbn': '9782882250209'}) == [{
        'label': 'isbn',
        'value': [
            '9782882250209'
        ]
    }]


def test_type():
    assert format_metadata('type', {
        'type': {
            'main': 'book',
            'sub': 'book_proceed'
        }
    }) == [{
        'label': 'type',
        'value': [
            'book > book_proceed'
        ]
    }]


def test_recid():
    assert format_metadata('recid', {'recid': '<id>'}) == [{
        'label': 'recid',
        'value': [
            '<id>'
        ]
    }]


def test_reroid():
    assert format_metadata('reroid', {
            'reroid': 'http://data.rero.ch/01-R1234'
        }) == [{
            'label': 'reroid',
            'value': [
                '<a href="http://data.rero.ch/01-R1234">01-R1234</a>'
            ]
        }]
# def test_other_title():
#     assert format_metadata(
#         'other_title',
#         {
#             'other_title': [{
#                 'main': '<maintitle>',
#                 'sub': '<subtitle>',
#                 'language': 'en'
#             }]
#         },
#         'en'
#     ) == '<maintitle> : <subtitle>'
