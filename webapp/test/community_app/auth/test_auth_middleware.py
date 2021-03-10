from datetime import datetime, timedelta
from unittest import mock
from unittest.mock import Mock, call

import pytest
from bh.core_utils.bh_exception import BHException
from bh.core_utils.test_utils import ServiceCallMock, mock_service_call
from bh_settings import get_settings
from django.conf import settings
from django.test import SimpleTestCase
from django.test.client import RequestFactory
from django.urls import reverse

from freezegun import freeze_time
from misago.users.models import AnonymousUser

from community_app.auth.middleware import PlatformTokenMiddleware
from community_app.constants import COOKIE_NAME_ACCESS_TOKEN, COOKIE_NAME_REFRESH_TOKEN


class UserMock:
    name = "user mock"
    is_superuser = False
    is_staff = False
    is_authenticated = True

    def __eq__(self, other):
        return isinstance(other, self.__class__)


class AdminUserMock(UserMock):
    name = "admin mock"
    is_superuser = True


@pytest.fixture
def get_request(community_path):
    request = RequestFactory().get(community_path)
    request.headers = {}
    request.headers["host"] = "foo.fake.com"
    request.headers["accept"] = "text/html"
    request.COOKIES = {}
    return request


@pytest.fixture
def get_response():
    return Mock()


# land on /, valid tokens, authenticated, same user
@mock_service_call(
    ServiceCallMock(
        "UserAccountAuthentication",
        "1",
        "find_with_tokens",
        return_value={"user_id": "a_user"},
    ),
    ServiceCallMock(
        "UserAccount",
        "1",
        "read",
        return_value={"uuid": "a_user_uuid"},
    )
)
@pytest.mark.parametrize("community_path", ["/"])
def test_middleware_valid_access_token_authenticated_root(mocks, get_request, get_response):
    get_request.user = UserMock()
    get_request.COOKIES[COOKIE_NAME_ACCESS_TOKEN] = "foo"
    get_request.COOKIES[COOKIE_NAME_REFRESH_TOKEN] = None
    get_request.user.social_auth = Mock(values=Mock(return_value=[{"uid": "a_user_uuid"}]))

    middleware = PlatformTokenMiddleware(get_response)
    response = middleware(get_request)

    assert not hasattr(get_request, "_platform_user_id")
    response.set_cookie.assert_not_called()


# land on /, valid tokens, not authenticated
@mock_service_call(
    ServiceCallMock(
        "UserAccountAuthentication",
        "1",
        "find_with_tokens",
        return_value={"user_id": "a_user"},
    )
)
@pytest.mark.parametrize("community_path", ["/"])
def test_middleware_valid_access_token_not_authenticated_root(mocks, get_request, get_response):
    get_request.user = AnonymousUser()
    get_request.COOKIES[COOKIE_NAME_ACCESS_TOKEN] = "foo"
    get_request.COOKIES[COOKIE_NAME_REFRESH_TOKEN] = None

    middleware = PlatformTokenMiddleware(get_response)
    response = middleware(get_request)

    assert not hasattr(get_request, "_platform_user_id")
    SimpleTestCase().assertRedirects(response, expected_url=reverse("social:complete", args=(["sleepio"])), fetch_redirect_response=False)


# land on /, valid tokens, authenticated, different user
@mock_service_call(
    ServiceCallMock(
        "UserAccountAuthentication",
        "1",
        "find_with_tokens",
        return_value={"user_id": "a_user"},
    ),
    ServiceCallMock(
        "UserAccount",
        "1",
        "read",
        return_value={"uuid": "a_user_uuid"},
    )
)
@pytest.mark.parametrize("community_path", ["/"])
def test_middleware_valid_access_token_authenticated_root_different_user(mocks, get_request, get_response):
    get_request.user = UserMock()
    get_request.COOKIES[COOKIE_NAME_ACCESS_TOKEN] = "foo"
    get_request.COOKIES[COOKIE_NAME_REFRESH_TOKEN] = None
    get_request.user.social_auth = Mock(values=Mock(return_value=[{"uid": "b_user_uuid"}]))

    middleware = PlatformTokenMiddleware(get_response)
    response = middleware(get_request)

    assert not hasattr(get_request, "_platform_user_id")
    SimpleTestCase().assertRedirects(response, expected_url=reverse("social:complete", args=(["sleepio"])), fetch_redirect_response=False)


# land on /complete/sleepio, valid tokens, not authenticated
@mock_service_call(
    ServiceCallMock(
        "UserAccountAuthentication",
        "1",
        "find_with_tokens",
        return_value={"user_id": "a_user"},
    )
)
@pytest.mark.parametrize("community_path", [reverse("social:complete", args=(["sleepio"]))])
def test_middleware_valid_access_token_not_authenticated_complete(mocks, get_request, get_response):
    get_request.user = AnonymousUser()
    get_request.COOKIES[COOKIE_NAME_ACCESS_TOKEN] = "foo"
    get_request.COOKIES[COOKIE_NAME_REFRESH_TOKEN] = None

    middleware = PlatformTokenMiddleware(get_response)
    response = middleware(get_request)

    assert get_request._platform_user_id == "a_user"
    assert not response.method_calls


# land on /complete/sleepio, valid tokens, authenticated
@mock_service_call(
    ServiceCallMock(
        "UserAccountAuthentication",
        "1",
        "find_with_tokens",
        return_value={"user_id": "a_user"},
    )
)
@mock.patch("community_app.auth.middleware.logout")
@pytest.mark.parametrize("community_path", [reverse("social:complete", args=(["sleepio"]))])
def test_middleware_valid_access_token_authenticated_complete(mocks, logout, get_request, get_response):
    get_request.user = UserMock()
    get_request.COOKIES[COOKIE_NAME_ACCESS_TOKEN] = "foo"
    get_request.COOKIES[COOKIE_NAME_REFRESH_TOKEN] = None

    middleware = PlatformTokenMiddleware(get_response)
    response = middleware(get_request)
    logout.assert_called()
    assert get_request.user == AnonymousUser()
    assert get_request._platform_user_id == "a_user"
    assert not response.method_calls


# land on /, refresh tokens
@freeze_time(datetime(1970, 1, 7, 12, 0))
@mock_service_call(
    ServiceCallMock(
        "UserAccountAuthentication",
        "1",
        "refresh_access_token",
        return_value={"access_token": "foo1", "refresh_token": "bar1"},
    ),
    ServiceCallMock(
        "UserAccountAuthentication",
        "1",
        "find_with_tokens",
        return_value={"user_id": "a_user"},
    ),
    ServiceCallMock(
        "UserAccount",
        "1",
        "read",
        return_value={"uuid": "a_user_uuid"},
    )
)
@pytest.mark.parametrize("community_path", ["/"])
def test_middleware_refresh_tokens(mocks, get_request, get_response):
    get_request.user = UserMock()
    get_request.COOKIES[COOKIE_NAME_ACCESS_TOKEN] = None
    get_request.COOKIES[COOKIE_NAME_REFRESH_TOKEN] = "bar"
    get_request.user.social_auth = Mock(values=Mock(return_value=[{"uid": "a_user_uuid"}]))

    middleware = PlatformTokenMiddleware(get_response)
    response = middleware(get_request)

    assert not hasattr(get_request, "_platform_user_id")

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


# land on / (HTML), can't authenticate
@mock_service_call(
    ServiceCallMock("UserAccountAuthentication", "1", "refresh_access_token", side_effect=raise_exception),
)
@mock.patch("community_app.auth.middleware.logout")
@pytest.mark.parametrize("community_path", ["/"])
def test_middleware_refresh_exception_logout_redirect(mocks, logout, get_request, get_response):
    get_request.user = UserMock()
    get_request.COOKIES[settings.SESSION_COOKIE_NAME] = "session"

    middleware = PlatformTokenMiddleware(get_response)
    response = middleware(get_request)

    assert get_request.user == AnonymousUser()
    assert not hasattr(get_request, "_platform_user_id")
    logout.assert_called_once()
    SimpleTestCase().assertRedirects(response, expected_url=get_settings("sleepio_app_url"), fetch_redirect_response=False)


# land on / (javascript), can't authenticate
@mock_service_call(
    ServiceCallMock("UserAccountAuthentication", "1", "refresh_access_token", side_effect=raise_exception),
)
@mock.patch("community_app.auth.middleware.logout")
@pytest.mark.parametrize("community_path", ["/"])
def test_middleware_refresh_exception_logout_unauthorized(mocks, logout, get_request, get_response):
    get_request.headers["accept"] = "app/js"

    get_request.user = UserMock()
    get_request.COOKIES[settings.SESSION_COOKIE_NAME] = "session"

    middleware = PlatformTokenMiddleware(get_response)
    response = middleware(get_request)

    assert get_request.user == AnonymousUser()
    assert not hasattr(get_request, "_platform_user_id")
    logout.assert_called_once()
    assert response.status_code == 401
    assert response["redirect_url"] == get_settings("sleepio_app_url")


# admins don't have special cookie handling
@pytest.mark.parametrize("community_path", ["/"])
def test_middleware_admin_user(get_request, get_response):
    get_request.user = AdminUserMock()
    get_request.COOKIES[COOKIE_NAME_ACCESS_TOKEN] = "foo"
    get_request.COOKIES[COOKIE_NAME_REFRESH_TOKEN] = "bar"

    middleware = PlatformTokenMiddleware(get_response)
    response = middleware(get_request)

    assert get_request.user == AdminUserMock()
    assert not hasattr(get_request, "_platform_user_id")
    response.set_cookie.assert_not_called()


# admin portal login doesn't have special cookie handling
@pytest.mark.parametrize("community_path", ["/admincp/"])
def test_middleware_admin_login(get_request, get_response):
    get_request.user = AnonymousUser()
    get_request.COOKIES[COOKIE_NAME_ACCESS_TOKEN] = "foo"
    get_request.COOKIES[COOKIE_NAME_REFRESH_TOKEN] = "bar"

    middleware = PlatformTokenMiddleware(get_response)
    response = middleware(get_request)

    assert get_request.user == AnonymousUser()
    assert not hasattr(get_request, "_platform_user_id")
    response.set_cookie.assert_not_called()
