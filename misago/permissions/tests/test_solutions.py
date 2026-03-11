import pytest
from django.core.exceptions import PermissionDenied

from ..solutions import (
    check_change_thread_solution_permission,
    check_clear_thread_solution_permission,
    check_lock_thread_solution_permission,
    check_select_thread_solution_permission,
    check_unlock_thread_solution_permission,
)


def test_check_lock_thread_solution_permission_passes_if_user_is_global_moderator(
    user_permissions_factory, moderator, thread
):
    permissions = user_permissions_factory(moderator)
    check_lock_thread_solution_permission(permissions, thread)


def test_check_lock_thread_solution_permission_passes_if_user_is_category_moderator(
    user_permissions_factory, category_moderator, thread
):
    permissions = user_permissions_factory(category_moderator)
    check_lock_thread_solution_permission(permissions, thread)


def test_check_lock_thread_solution_permission_fails_user(
    user_permissions_factory, user, thread
):
    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_lock_thread_solution_permission(permissions, thread)


def test_check_lock_thread_solution_permission_fails_anonymous_user(
    user_permissions_factory, anonymous_user, thread
):
    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_lock_thread_solution_permission(permissions, thread)


def test_check_unlock_thread_solution_permission_passes_if_user_is_global_moderator(
    user_permissions_factory, moderator, thread
):
    permissions = user_permissions_factory(moderator)
    check_unlock_thread_solution_permission(permissions, thread)


def test_check_unlock_thread_solution_permission_passes_if_user_is_category_moderator(
    user_permissions_factory, category_moderator, thread
):
    permissions = user_permissions_factory(category_moderator)
    check_unlock_thread_solution_permission(permissions, thread)


def test_check_unlock_thread_solution_permission_fails_user(
    user_permissions_factory, user, thread
):
    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_unlock_thread_solution_permission(permissions, thread)


def test_check_unlock_thread_solution_permission_fails_anonymous_user(
    user_permissions_factory, anonymous_user, thread
):
    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_unlock_thread_solution_permission(permissions, thread)
