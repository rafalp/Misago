from django.http import Http404
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from ...acl.useracl import get_user_acl
from ...conf.dynamicsettings import DynamicSettings
from ...conftest import get_cache_versions
from ...users.models import AnonymousUser
from ..middleware import ExceptionHandlerMiddleware


def create_request():
    request = RequestFactory().get(reverse("misago:index"))
    request.cache_versions = get_cache_versions()
    request.settings = DynamicSettings(request.cache_versions)
    request.user = AnonymousUser()
    request.user_acl = get_user_acl(request.user, request.cache_versions)
    request.include_frontend_context = True
    request.frontend_context = {}
    request.socialauth = {}
    return request


class ExceptionHandlerMiddlewareTests(TestCase):
    def test_middleware_returns_response_for_supported_exception(self):
        """Middleware returns HttpResponse for supported exception"""
        middleware = ExceptionHandlerMiddleware()
        exception = Http404()
        assert middleware.process_exception(create_request(), exception)

    def test_middleware_returns_none_for_non_supported_exception(self):
        """Middleware returns None for non-supported exception"""
        middleware = ExceptionHandlerMiddleware()
        exception = TypeError()
        assert middleware.process_exception(create_request(), exception) is None
