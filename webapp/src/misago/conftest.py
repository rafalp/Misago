from django.contrib.auth import load_backend
import pytest

from bh.core_utils.test_utils import mock_service_calls, ServiceCallMock

from .acl import ACL_CACHE, useracl
from .admin.auth import authorize_admin
from .categories.models import Category
from .conf import SETTINGS_CACHE
from .conf.dynamicsettings import DynamicSettings
from .conf.staticsettings import StaticSettings
from .menus import MENU_ITEMS_CACHE
from .socialauth import SOCIALAUTH_CACHE
from .test import MisagoClient
from .themes import THEME_CACHE
from .threads.test import post_thread
from .users import BANS_CACHE
from .users.models import AnonymousUser
from .users.test import create_test_superuser, create_test_user

from community_app.constants import COOKIE_NAME_ACCESS_TOKEN


def get_cache_versions():
    return {
        ACL_CACHE: "abcdefgh",
        BANS_CACHE: "abcdefgh",
        SETTINGS_CACHE: "abcdefgh",
        SOCIALAUTH_CACHE: "abcdefgh",
        THEME_CACHE: "abcdefgh",
        MENU_ITEMS_CACHE: "abcdefgh",
    }


@pytest.fixture
def cache_versions():
    return get_cache_versions()


@pytest.fixture
def dynamic_settings(db, cache_versions):
    return DynamicSettings(cache_versions)


@pytest.fixture
def settings():
    return StaticSettings()


@pytest.fixture
def user_password():
    return "p4ssw0rd!"


@pytest.fixture
def anonymous_user():
    return AnonymousUser()


@pytest.fixture
def anonymous_user_acl(anonymous_user, cache_versions):
    return useracl.get_user_acl(anonymous_user, cache_versions)


@pytest.fixture
def user(db, user_password):
    return create_test_user("User", "user@example.com", user_password)


@pytest.fixture
def user_acl(user, cache_versions):
    return useracl.get_user_acl(user, cache_versions)


@pytest.fixture
def other_user(db, user_password):
    return create_test_user("OtherUser", "otheruser@example.com", user_password)


@pytest.fixture
def other_user_acl(other_user, cache_versions):
    return useracl.get_user_acl(other_user, cache_versions)


@pytest.fixture
def staffuser(db, user_password):
    user = create_test_superuser("Staffuser", "staffuser@example.com", user_password)
    user.is_superuser = False
    user.save()
    return user


@pytest.fixture
def staffuser_acl(staffuser, cache_versions):
    return useracl.get_user_acl(staffuser, cache_versions)


@pytest.fixture
def other_staffuser(db, user_password):
    user = create_test_superuser(
        "OtherStaffuser", "otherstaffuser@example.com", user_password
    )

    user.is_superuser = False
    user.save()
    return user


@pytest.fixture
def superuser(db, user_password):
    return create_test_superuser("Superuser", "superuser@example.com", user_password)


@pytest.fixture
def superuser_acl(superuser, cache_versions):
    return useracl.get_user_acl(superuser, cache_versions)


@pytest.fixture
def other_superuser(db, user_password):
    return create_test_superuser(
        "OtherSuperuser", "othersuperuser@example.com", user_password
    )


@pytest.fixture
def client():
    client = MisagoClient()
    client.cookies[COOKIE_NAME_ACCESS_TOKEN] = "at"
    return client


@pytest.fixture(autouse=True)
def service_mocks():
    with mock_service_calls([
        ServiceCallMock("UserAccountAuthentication", "1", "find_with_tokens", return_value={"user_id": 123}),
        ServiceCallMock("UserAccount", "1", "read", return_value={"uuid": "a_user_uuid"}),
    ]):
        yield


@pytest.fixture
def user_client(mocker, client, user):
    client.force_login(user)

    # Our middleware requires a social auth
    backend = load_backend("community_app.auth.backend.SleepioAuth")
    backend.strategy.storage.user.create_social_auth(user, "a_user_uuid", backend.name)

    session = client.session
    session.save()
    return client


@pytest.fixture
def admin_client(mocker, client, superuser):
    client.force_login(superuser)
    session = client.session
    authorize_admin(mocker.Mock(session=session, user=superuser))
    session.save()
    return client


@pytest.fixture
def staff_client(mocker, client, staffuser):
    client.force_login(staffuser)
    session = client.session
    authorize_admin(mocker.Mock(session=session, user=staffuser))
    session.save()
    return client


@pytest.fixture
def root_category(db):
    return Category.objects.root_category()


@pytest.fixture
def default_category(db):
    return Category.objects.get(slug="first-category")


@pytest.fixture
def thread(default_category):
    return post_thread(default_category)


@pytest.fixture
def hidden_thread(default_category):
    return post_thread(default_category, is_hidden=True)


@pytest.fixture
def unapproved_thread(default_category):
    return post_thread(default_category, is_unapproved=True)


@pytest.fixture
def post(thread):
    return thread.first_post


@pytest.fixture
def user_thread(default_category, user):
    return post_thread(default_category, poster=user)


@pytest.fixture
def user_hidden_thread(default_category, user):
    return post_thread(default_category, poster=user, is_hidden=True)


@pytest.fixture
def user_unapproved_thread(default_category, user):
    return post_thread(default_category, poster=user, is_unapproved=True)


@pytest.fixture
def other_user_thread(default_category, other_user):
    return post_thread(default_category, poster=other_user)


@pytest.fixture
def other_user_hidden_thread(default_category, other_user):
    return post_thread(default_category, poster=other_user, is_hidden=True)


@pytest.fixture
def other_user_unapproved_thread(default_category, other_user):
    return post_thread(default_category, poster=other_user, is_unapproved=True)
