from unittest.mock import patch

from ..user import get_user_permissions


@patch("misago.permissions.user.build_user_permissions")
@patch("misago.permissions.user.cache")
def test_get_user_permissions_builds_user_permissions_on_cache_miss(
    cache_mock, build_user_permissions, cache_versions, user
):
    build_user_permissions.return_value = {"build_permissions": True}
    cache_mock.get.return_value = None

    permissions = get_user_permissions(user, cache_versions)
    assert permissions["build_permissions"]

    cache_mock.get.assert_called_once()
    cache_mock.set.assert_called_once()
    build_user_permissions.assert_called_once()


@patch("misago.permissions.user.build_user_permissions")
@patch("misago.permissions.user.cache")
def test_get_user_permissions_uses_cached_permissions_on_cache_hit(
    cache_mock, build_user_permissions, cache_versions, user
):
    cache_mock.get.return_value = {"cached_permissions": True}

    permissions = get_user_permissions(user, cache_versions)
    assert permissions["cached_permissions"]

    cache_mock.get.assert_called_once()
    cache_mock.set.assert_not_called()
    build_user_permissions.assert_not_called()


@patch("misago.permissions.user.build_user_permissions")
@patch("misago.permissions.user.cache")
def test_get_user_permissions_builds_anonymous_user_permissions_on_cache_miss(
    cache_mock, build_user_permissions, cache_versions, db, anonymous_user
):
    build_user_permissions.return_value = {"build_permissions": True}
    cache_mock.get.return_value = None

    permissions = get_user_permissions(anonymous_user, cache_versions)
    assert permissions["build_permissions"]

    cache_mock.get.assert_called_once()
    cache_mock.set.assert_called_once()
    build_user_permissions.assert_called_once()


@patch("misago.permissions.user.build_user_permissions")
@patch("misago.permissions.user.cache")
def test_get_user_permissions_uses_anonymous_cached_permissions_on_cache_hit(
    cache_mock, build_user_permissions, cache_versions, db, anonymous_user
):
    cache_mock.get.return_value = {"cached_permissions": True}

    permissions = get_user_permissions(anonymous_user, cache_versions)
    assert permissions["cached_permissions"]

    cache_mock.get.assert_called_once()
    cache_mock.set.assert_not_called()
    build_user_permissions.assert_not_called()
