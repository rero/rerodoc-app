# -*- coding: utf-8 -*-
import pytest

from rerodoc_app.udc.udc import UnsupportedError, extract_rdf, \
    get_long_names, get_udc, update_udc

slow = pytest.mark.skipif(
    not pytest.config.getoption('--runslow'),
    reason='need --runslow option to run'
)


class TestUDC:

    @slow
    def test_rdf_udc_import(self):
        udc = extract_rdf()
        assert udc.get('004', {}).get('uri') == 'http://udcdata.info/013566'

    @slow
    def test_update_udc(self):
        assert update_udc()

    def test_simple(self):
        assert get_udc('004').get('uri') == [
            'http://udcdata.info/013566'
        ]

    def test_multiple(self):
        assert get_udc('73/77').get('uri') == [
            'http://udcdata.info/065174',
            'http://udcdata.info/065213',
            'http://udcdata.info/065280',
            'http://udcdata.info/065294',
            'http://udcdata.info/065307'
        ]

    def test_udc_parent(self):
        assert get_udc('614.253.5').get('uri') == [
            'http://udcdata.info/038191'
        ]

    def test_hierarchy(self):
        assert get_udc('616').get('parent') == '61'

    def test_wrong_value(self):
        with pytest.raises(UnsupportedError):
            get_udc('foo')

    def test_long_names(self):
        assert get_long_names().get('33', {}).get('name') == \
               u'Arts, Human and Social Science ▸ Economics (33)'
