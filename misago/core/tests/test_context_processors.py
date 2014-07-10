from django.test import TestCase
from misago.core import context_processors


class MockRequest(object):
    def __init__(self, secure, host):
        self.secure = secure
        self.host = host

    def is_secure(self):
        return self.secure

    def get_host(self):
        return self.host


class SiteAddressTests(TestCase):
    def test_site_address_for_http(self):
        """Correct SITE_ADDRESS set for HTTP request"""
        http_somewhere_com = MockRequest(False, 'somewhere.com')
        self.assertEqual(
            context_processors.site_address(http_somewhere_com),
            {
                'SITE_ADDRESS': 'http://somewhere.com',
                'SITE_HOST': 'somewhere.com',
                'SITE_PROTOCOL': 'http',
            })

    def test_site_address_for_https(self):
        """Correct SITE_ADDRESS set for HTTPS request"""
        https_somewhere_com = MockRequest(True, 'somewhere.com')
        self.assertEqual(
            context_processors.site_address(https_somewhere_com),
            {
                'SITE_ADDRESS': 'https://somewhere.com',
                'SITE_HOST': 'somewhere.com',
                'SITE_PROTOCOL': 'https',
            })
