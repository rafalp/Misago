from django.http import Http404
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from misago.core.middleware.exceptionhandler import ExceptionHandlerMiddleware
from misago.users.models import AnonymousUser


class ExceptionHandlerMiddlewareTests(TestCase):
    def setUp(self):
        self.request = RequestFactory().get(reverse('misago:index'))
        self.request.user = AnonymousUser()
        self.request.include_frontend_context = True
        self.request.frontend_context = {}

    def test_middleware_returns_response_for_supported_exception(self):
        """Middleware returns HttpResponse for supported exception"""
        exception = Http404()
        middleware = ExceptionHandlerMiddleware()

        self.assertTrue(middleware.process_exception(self.request, exception))

    def test_middleware_returns_none_for_non_supported_exception(self):
        """Middleware returns None for non-supported exception"""
        exception = TypeError()
        middleware = ExceptionHandlerMiddleware()

        self.assertFalse(middleware.process_exception(self.request, exception))
