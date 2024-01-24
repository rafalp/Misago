from unittest.mock import Mock

import pytest

from ...permissions.proxy import UserPermissionsProxy
from ..context import create_parser_context


def test_create_parser_context_creates_context_from_request(
    dynamic_settings, cache_versions, user
):
    request = Mock(
        settings=dynamic_settings,
        cache_versions=cache_versions,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )

    context = create_parser_context(request)
    assert context.request is request
    assert context.forum_address
    assert context.user is request.user
    assert context.user_permissions is request.user_permissions
    assert context.settings is dynamic_settings
    assert context.cache_versions is cache_versions


def test_create_parser_context_creates_context_with_empty_content_type(
    dynamic_settings, cache_versions, user
):
    request = Mock(
        settings=dynamic_settings,
        cache_versions=cache_versions,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )

    context = create_parser_context(request)
    assert context.content_type is None


def test_create_parser_context_creates_context_with_given_content_type(
    dynamic_settings, cache_versions, user
):
    request = Mock(
        settings=dynamic_settings,
        cache_versions=cache_versions,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )

    context = create_parser_context(request, content_type="TEST")
    assert context.content_type == "TEST"


def test_create_parser_context_creates_context_with_empty_plugin_data(
    dynamic_settings, cache_versions, user
):
    request = Mock(
        settings=dynamic_settings,
        cache_versions=cache_versions,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )

    context = create_parser_context(request)
    assert context.plugin_data == {}


def test_create_parser_context_creates_context_without_request(
    dynamic_settings, cache_versions, user
):
    user_permissions = UserPermissionsProxy(user, cache_versions)

    context = create_parser_context(
        user_permissions=user_permissions,
        settings=dynamic_settings,
        cache_versions=cache_versions,
    )

    assert context.request is None
    assert context.forum_address
    assert context.user is user
    assert context.user_permissions is user_permissions
    assert context.settings is dynamic_settings
    assert context.cache_versions is cache_versions


def test_create_parser_context_creates_context_with_explicit_user_permissions(
    dynamic_settings, cache_versions, user, other_user
):
    request = Mock(
        settings=dynamic_settings,
        cache_versions=cache_versions,
        user=user,
        user_permissions=UserPermissionsProxy(user, cache_versions),
    )

    other_user_permissions = UserPermissionsProxy(other_user, cache_versions)
    context = create_parser_context(request, user_permissions=other_user_permissions)
    assert context.user is other_user
    assert context.user_permissions is other_user_permissions


def test_create_parser_context_raises_error_if_user_permissions_is_missing(
    dynamic_settings, cache_versions
):
    with pytest.raises(TypeError):
        create_parser_context(
            settings=dynamic_settings,
            cache_versions=cache_versions,
        )


def test_create_parser_context_raises_error_if_settings_is_missing(
    dynamic_settings, cache_versions, user
):
    user_permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(TypeError):
        create_parser_context(
            user_permissions=user_permissions,
            cache_versions=cache_versions,
        )


def test_create_parser_context_raises_error_if_cache_versions_is_missing(
    dynamic_settings, cache_versions, user
):
    user_permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(TypeError):
        create_parser_context(
            user_permissions=user_permissions,
            dynamic_settings=dynamic_settings,
        )
