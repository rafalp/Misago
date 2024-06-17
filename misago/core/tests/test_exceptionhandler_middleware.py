from django.http import Http404
from django.test.client import RequestFactory
from django.urls import reverse

from ...acl.useracl import get_user_acl
from ...categories.proxy import CategoriesProxy
from ...conf.dynamicsettings import DynamicSettings
from ...conftest import get_cache_versions
from ...permissions.proxy import UserPermissionsProxy
from ...users.models import AnonymousUser
from ..middleware import ExceptionHandlerMiddleware


def create_request():
    request = RequestFactory().get(reverse("misago:index"))
    request.cache_versions = get_cache_versions()
    request.settings = DynamicSettings(request.cache_versions)
    request.user = AnonymousUser()
    request.user_acl = get_user_acl(request.user, request.cache_versions)
    request.user_permissions = UserPermissionsProxy(
        request.user, request.cache_versions
    )
    request.categories = CategoriesProxy(
        request.user_permissions, request.cache_versions
    )
    request.include_frontend_context = True
    request.frontend_context = {}
    request.socialauth = {}
    request.is_htmx = False
    return request


def get_response(*_args):
    raise NotImplementedError()


def test_exception_handler_middleware_returns_response_for_supported_exception(db):
    """Middleware returns HttpResponse for supported exception"""
    middleware = ExceptionHandlerMiddleware(get_response)
    exception = Http404()
    assert middleware.process_exception(create_request(), exception)


def test_exception_handler_middleware_returns_none_for_non_supported_exception(db):
    """Middleware returns None for non-supported exception"""
    middleware = ExceptionHandlerMiddleware(get_response)
    exception = TypeError()
    assert middleware.process_exception(create_request(), exception) is None
