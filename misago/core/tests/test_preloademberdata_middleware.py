from django.test import TestCase
from misago.core.middleware.preloademberdata import PreloadEmberDataMiddleware


class MockRequest(object):
    pass


class PreloadEmberDataMiddlewareTests(TestCase):
    def test_middleware_sets_preloaded_dict(self):
        """Middleware sets preloaded_ember_data dict on request"""
        request = MockRequest()

        PreloadEmberDataMiddleware().process_request(request)
        self.assertEqual(request.preloaded_ember_data, {})
