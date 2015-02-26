from django.test import TestCase
from misago.conf.middleware import PreloadConfigMiddleware


class MockRequest(object):
    def __init__(self):
        self.preloaded_ember_data = {}


class PreloadConfigMiddlewareTests(TestCase):
    def test_middleware_preloads_configuration(self):
        """Middleware sets keys in preloaded_ember_data dict on request"""
        request = MockRequest()

        PreloadConfigMiddleware().process_request(request)

        MIDDLEWARE_KEYS = (
            'misagoSettings',

            'staticUrl',
            'mediaUrl',
        )

        for key in MIDDLEWARE_KEYS:
            self.assertIn(key, request.preloaded_ember_data)
