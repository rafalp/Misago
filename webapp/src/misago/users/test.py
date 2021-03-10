import pytest

from django.contrib.auth import get_user_model, load_backend
from django.test import TestCase

from bh.core_utils.test_utils import mock_service_calls, ServiceCallMock

from community_app.constants import COOKIE_NAME_ACCESS_TOKEN

from .models import AnonymousUser, Online

User = get_user_model()


class PlatformTestCase(TestCase):

    @pytest.fixture
    def service_mocks(self):
        with mock_service_calls([
            ServiceCallMock("UserAccountAuthentication", "1", "find_with_tokens", return_value={"user_id": 123}),
            ServiceCallMock("UserAccount", "1", "read", return_value={"uuid": "a_user_uuid"}),
        ]):
            yield

    def setUp(self):
        super().setUp()
        self.client.cookies[COOKIE_NAME_ACCESS_TOKEN] = "at"

class UserTestCase(PlatformTestCase):
    USER_PASSWORD = "Pass.123"
    USER_IP = "127.0.0.1"

    def setUp(self):
        super().setUp()
        self.get_initial_user()

    def get_initial_user(self):
        self.user = self.get_anonymous_user()

    def get_anonymous_user(self):
        return AnonymousUser()

    def get_authenticated_user(self):
        return create_test_user(
            "TestUser", "test@user.com", self.USER_PASSWORD, joined_from_ip=self.USER_IP
        )

    def get_superuser(self):
        return create_test_superuser(
            "TestSuperUser",
            "test@superuser.com",
            self.USER_PASSWORD,
            joined_from_ip=self.USER_IP,
        )

    def login_user(self, user, password=None, uid=None):
        self.client.force_login(user)

        # Our middleware requires a social auth
        backend = load_backend("community_app.auth.backend.SleepioAuth")
        backend.strategy.storage.user.create_social_auth(user, uid if uid else "a_user_uuid", backend.name)

    def logout_user(self):
        if self.user.is_authenticated:
            Online.objects.filter(user=self.user).delete()
        self.client.logout()


class AuthenticatedUserTestCase(UserTestCase):

    def get_initial_user(self):
        self.user = self.get_authenticated_user()
        self.login_user(self.user)

    def reload_user(self):
        self.user.refresh_from_db()


class SuperUserTestCase(AuthenticatedUserTestCase):
    def get_initial_user(self):
        self.user = self.get_superuser()
        self.login_user(self.user)


def create_test_user(username, email, password=None, **extra_fields):
    """Faster alternative to regular `create_user` followed by `setup_new_user`"""
    if "avatars" not in extra_fields:
        extra_fields["avatars"] = user_placeholder_avatars

    return User.objects.create_user(username, email, password, **extra_fields)


def create_test_superuser(username, email, password=None, **extra_fields):
    """Faster alternative to regular `create_superuser` followed by `setup_new_user`"""
    if "avatars" not in extra_fields:
        extra_fields["avatars"] = user_placeholder_avatars

    return User.objects.create_superuser(username, email, password, **extra_fields)


user_placeholder_avatars = [
    {"size": 400, "url": "http://placekitten.com/400/400"},
    {"size": 200, "url": "http://placekitten.com/200/200"},
    {"size": 100, "url": "http://placekitten.com/100/100"},
]
