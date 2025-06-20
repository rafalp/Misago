import pytest
from django.contrib.auth.models import AnonymousUser

from ..permissions.proxy import UserPermissionsProxy
from ..users.models import User


@pytest.fixture
def user_permissions_factory(cache_versions):
    def _user_permissions_factory(user: AnonymousUser | User):
        return UserPermissionsProxy(user, cache_versions)

    return _user_permissions_factory


@pytest.fixture
def user_permissions(user, user_permissions_factory):
    return user_permissions_factory(user)


@pytest.fixture
def anonymous_user_permissions(anonymous_user, user_permissions_factory):
    return user_permissions_factory(anonymous_user)
