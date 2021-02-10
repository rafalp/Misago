from datetime import datetime, timedelta
from unittest import mock
from unittest.mock import Mock, call

import pytest
from bh.core_utils.bh_exception import BHException
from bh.core_utils.test_utils import ServiceCallMock, mock_service_call
from bh_settings import get_settings
from django.conf import settings
from django.test.client import RequestFactory
from freezegun import freeze_time
from misago.users.models import AnonymousUser

from community_app.auth.middleware import PlatformTokenMiddleware
from community_app.constants import COOKIE_NAME_ACCESS_TOKEN, COOKIE_NAME_REFRESH_TOKEN


@pytest.fixture
def get_request():
    request = RequestFactory().get("/")
    request.headers = {}
    request.headers["host"] = "foo.fake.com"
    request.COOKIES = {}
    return request


@pytest.fixture
def get_response():
    return Mock()


@mock_service_call(ServiceCallMock("UserAccountAuthentication", "1", "find_with_tokens", return_value={"user_id": "a_user"},))
def test_middleware_valid_access_token(mocks, get_request, get_response):
    get_request.user = AnonymousUser()
    get_request.COOKIES[COOKIE_NAME_ACCESS_TOKEN] = "foo"
    get_request.COOKIES[COOKIE_NAME_REFRESH_TOKEN] = None

    middleware = PlatformTokenMiddleware(get_response)
    response = middleware(get_request)

    assert get_request._platform_user_id == "a_user"
    assert not response.method_calls


@freeze_time(datetime(1970, 1, 7, 12, 0))
@mock_service_call(
    ServiceCallMock("UserAccountAuthentication", "1", "refresh_access_token", return_value={"access_token": "foo1", "refresh_token": "bar1"},),
    ServiceCallMock("UserAccountAuthentication", "1", "find_with_tokens", return_value={"user_id": "a_user"},),
)
def test_middleware_refresh_tokens(mocks, get_request, get_response):
    get_request.user = AnonymousUser()
    get_request.COOKIES[COOKIE_NAME_ACCESS_TOKEN] = None
    get_request.COOKIES[COOKIE_NAME_REFRESH_TOKEN] = "bar"

    middleware = PlatformTokenMiddleware(get_response)
    response = middleware(get_request)

    assert get_request._platform_user_id == "a_user"

    calls = [
        call(
            COOKIE_NAME_ACCESS_TOKEN,
            "foo1",
            expires=(datetime(1970, 1, 7, 12, 0) + timedelta(seconds=get_settings("access_token_cookie_expiration_seconds"))),
            domain=".fake.com",
            secure=get_settings("secure_cookies", True),
            httponly=True,
        ),
        call(
            COOKIE_NAME_REFRESH_TOKEN,
            "bar1",
            expires=(datetime(1970, 1, 7, 12, 0) + timedelta(days=get_settings("refresh_token_cookie_expiration_days"))),
            domain=".fake.com",
            secure=get_settings("secure_cookies", True),
            httponly=True,
        ),
    ]
    response.set_cookie.assert_has_calls(calls)


def raise_exception(*args, **kwargs):
    class UserNotAuthenticated(BHException):
        # The page or resource you were trying to access can not be loaded until
        # you first log-in with a valid username and password.
        STATUS_CODE = 401
        SHOULD_ALERT = False

    raise UserNotAuthenticated


@mock_service_call(ServiceCallMock("UserAccountAuthentication", "1", "refresh_access_token", side_effect=raise_exception),)
@mock.patch("community_app.auth.middleware.logout")
def test_middleware_refresh_exception_logout(mocks, logout, get_request, get_response):
    class UserMock:
        name = "user mock"
        is_superuser = False

    get_request.user = UserMock()
    get_request.COOKIES[settings.SESSION_COOKIE_NAME] = "session"

    middleware = PlatformTokenMiddleware(get_response)
    response = middleware(get_request)

    assert get_request.user == AnonymousUser()
    assert not hasattr(get_request, "_platform_user_id")
    logout.assert_called_once()
    response.set_cookie.assert_not_called()


def test_middleware_admin_user(get_request, get_response):
    class AdminUserMock:
        name = "admin mock"
        is_superuser = True

        def __eq__(self, other):
            return isinstance(other, self.__class__)

    get_request.user = AdminUserMock()
    get_request.COOKIES[COOKIE_NAME_ACCESS_TOKEN] = "foo"
    get_request.COOKIES[COOKIE_NAME_REFRESH_TOKEN] = "bar"

    middleware = PlatformTokenMiddleware(get_response)
    response = middleware(get_request)

    assert get_request.user == AdminUserMock()
    assert not hasattr(get_request, "_platform_user_id")
    response.set_cookie.assert_not_called()
