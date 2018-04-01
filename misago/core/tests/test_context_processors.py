from django.test import TestCase
from django.utils import translation

from misago.core import context_processors


class MockRequest(object):
    path = '/'

    def __init__(self, secure, host):
        self.secure = secure
        self.host = host

    def is_secure(self):
        return self.secure

    def get_host(self):
        return self.host


class MetaMockRequest(object):
    def __init__(self, meta):
        self.META = meta


class MomentjsLocaleTests(TestCase):
    def test_momentjs_locale(self):
        """momentjs_locale adds MOMENTJS_LOCALE_URL to context"""
        with translation.override('no-no'):
            self.assertEqual(
                context_processors.momentjs_locale(True), {
                    'MOMENTJS_LOCALE_URL': None,
                }
            )

        with translation.override('en-us'):
            self.assertEqual(
                context_processors.momentjs_locale(True), {
                    'MOMENTJS_LOCALE_URL': None,
                }
            )

        with translation.override('de'):
            self.assertEqual(
                context_processors.momentjs_locale(True), {
                    'MOMENTJS_LOCALE_URL': 'misago/momentjs/de.js',
                }
            )

        with translation.override('pl-de'):
            self.assertEqual(
                context_processors.momentjs_locale(True), {
                    'MOMENTJS_LOCALE_URL': 'misago/momentjs/pl.js',
                }
            )


class SiteAddressTests(TestCase):
    def test_site_address_for_http(self):
        """Correct SITE_ADDRESS set for HTTP request"""
        mock_request = MockRequest(False, 'somewhere.com')
        self.assertEqual(
            context_processors.site_address(mock_request), {
                'REQUEST_PATH': '/',
                'SITE_ADDRESS': 'http://somewhere.com',
                'SITE_HOST': 'somewhere.com',
                'SITE_PROTOCOL': 'http',
            }
        )

    def test_site_address_for_https(self):
        """Correct SITE_ADDRESS set for HTTPS request"""
        mock_request = MockRequest(True, 'somewhere.com')
        self.assertEqual(
            context_processors.site_address(mock_request), {
                'REQUEST_PATH': '/',
                'SITE_ADDRESS': 'https://somewhere.com',
                'SITE_HOST': 'somewhere.com',
                'SITE_PROTOCOL': 'https',
            }
        )
