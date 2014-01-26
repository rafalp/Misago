from django.core.urlresolvers import reverse
from django.http import Http404
from django.test import TestCase
from django.test.client import RequestFactory
from misago.views.middleware import MisagoExceptionHandlerMiddleware


class MisagoExceptionHandlerMiddlewareTests(TestCase):
    def setUp(self):
        self.request = RequestFactory().get(reverse('forum_index'))

    def test_middleware_returns_response_for_supported_exception(self):
        "Middleware returns HttpResponse for supported exception"
        exception = Http404()
        middleware = MisagoExceptionHandlerMiddleware()

        self.assertTrue(middleware.process_exception(self.request, exception))

    def test_middleware_returns_none_for_non_supported_exception(self):
        """Middleware returns None for non-supported exception"""
        exception = TypeError()
        middleware = MisagoExceptionHandlerMiddleware()

        self.assertFalse(middleware.process_exception(self.request, exception))
