import pytest

from ...permissions.proxy import UserPermissionsProxy


@pytest.fixture
def user_request(rf, cache_versions, dynamic_settings, user):
    request = rf.post("/post/")

    request.cache_versions = cache_versions
    request.settings = dynamic_settings
    request.user = user
    request.user_permissions = UserPermissionsProxy(user, cache_versions)

    return request
