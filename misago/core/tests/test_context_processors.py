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
        mock_request = MockRequest(False, 'somewhere.com')
        self.assertEqual(
            context_processors.site_address(mock_request),
            {
                'SITE_ADDRESS': 'http://somewhere.com',
                'SITE_HOST': 'somewhere.com',
                'SITE_PROTOCOL': 'http',
            })

    def test_site_address_for_https(self):
        """Correct SITE_ADDRESS set for HTTPS request"""
        mock_request = MockRequest(True, 'somewhere.com')
        self.assertEqual(
            context_processors.site_address(mock_request),
            {
                'SITE_ADDRESS': 'https://somewhere.com',
                'SITE_HOST': 'somewhere.com',
                'SITE_PROTOCOL': 'https',
            })


class PreloadedDataTests(TestCase):
    def test_preloaded_ember_data(self):
        """preloaded_ember_data is available in templates"""
        mock_request = MockRequest(False, 'somewhere.com')
        mock_request.preloaded_ember_data = {'someValue': 'Something'}

        self.assertEqual(
            context_processors.preloaded_ember_data(mock_request),
            {'preloaded_ember_data': {'someValue': 'Something'}})
