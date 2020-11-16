from django.test import TestCase

from ..middleware import FrontendContextMiddleware


class MockRequest:
    pass


class FrontendContextMiddlewareTests(TestCase):
    def test_middleware_frontend_context_dict(self):
        """Middleware sets frontend_context dict on request"""
        request = MockRequest()

        FrontendContextMiddleware().process_request(request)
        self.assertEqual(request.frontend_context, {})
