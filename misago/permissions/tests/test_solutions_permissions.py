from datetime import timedelta

import pytest
from django.core.exceptions import PermissionDenied

from ...solutions.solutions import lock_thread_solution, select_thread_solution
from ..solutions import (
    check_change_thread_solution_permission,
    check_clear_thread_solution_permission,
    check_lock_thread_solution_permission,
    check_select_thread_solution_permission,
    check_unlock_thread_solution_permission,
)


def test_check_select_thread_solution_permission_fails_for_global_moderator_for_own_thread_in_category_with_disabled_solutions(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
):
    default_category.enable_solutions = False
    default_category.save()

    thread = thread_factory(default_category, starter=moderator)
    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(moderator)

    with pytest.raises(PermissionDenied):
        check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_fails_for_global_moderator_for_other_user_thread_in_category_with_disabled_solutions(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = False
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(moderator)

    with pytest.raises(PermissionDenied):
        check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_fails_for_global_moderator_for_deleted_user_thread_in_category_with_disabled_solutions(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
    thread,
):
    default_category.enable_solutions = False
    default_category.save()

    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(moderator)

    with pytest.raises(PermissionDenied):
        check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_fails_for_category_moderator_for_own_thread_in_category_with_disabled_solutions(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
):
    default_category.enable_solutions = False
    default_category.save()

    thread = thread_factory(default_category, starter=category_moderator)
    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(category_moderator)

    with pytest.raises(PermissionDenied):
        check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_fails_for_category_moderator_for_other_user_thread_in_category_with_disabled_solutions(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = False
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(category_moderator)

    with pytest.raises(PermissionDenied):
        check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_fails_for_category_moderator_for_deleted_user_thread_in_category_with_disabled_solutions(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
    thread,
):
    default_category.enable_solutions = False
    default_category.save()

    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(category_moderator)

    with pytest.raises(PermissionDenied):
        check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_fails_for_user_for_own_thread_in_category_with_disabled_solutions(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
):
    default_category.enable_solutions = False
    default_category.save()

    thread = thread_factory(default_category, starter=user)
    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_fails_for_user_for_other_user_thread_in_category_with_disabled_solutions(
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = False
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_fails_for_user_for_deleted_user_thread_in_category_with_disabled_solutions(
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
    thread,
):
    default_category.enable_solutions = False
    default_category.save()

    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_fails_for_anonymous_user_for_other_user_thread_in_category_with_disabled_solutions(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    guests_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = False
    default_category.save()

    guests_group.can_select_own_thread_solutions = True
    guests_group.save()

    solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_fails_for_anonymous_user_for_deleted_user_thread_in_category_with_disabled_solutions(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    guests_group,
    default_category,
    thread,
):
    default_category.enable_solutions = False
    default_category.save()

    guests_group.can_select_own_thread_solutions = True
    guests_group.save()

    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_passes_for_global_moderator_for_own_thread(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    thread = thread_factory(default_category, starter=moderator)
    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(moderator)
    check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_passes_for_global_moderator_for_other_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(moderator)
    check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_passes_for_global_moderator_for_deleted_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(moderator)
    check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_passes_for_category_moderator_for_own_thread(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    thread = thread_factory(default_category, starter=category_moderator)
    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(category_moderator)
    check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_passes_for_category_moderator_for_other_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(category_moderator)
    check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_passes_for_category_moderator_for_deleted_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(category_moderator)
    check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_passes_for_user_for_own_thread(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    thread = thread_factory(default_category, starter=user)
    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(user)
    check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_fails_for_user_for_other_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_fails_for_user_for_deleted_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_fails_for_anonymous_user_for_other_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    guests_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    guests_group.can_select_own_thread_solutions = True
    guests_group.save()

    solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_fails_for_anonymous_user_for_deleted_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    guests_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    guests_group.can_select_own_thread_solutions = True
    guests_group.save()

    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_passes_for_global_moderator_without_permission_for_own_thread(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    moderators_group,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    moderators_group.can_select_own_thread_solutions = False
    moderators_group.save()

    thread = thread_factory(default_category, starter=moderator)
    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(moderator)
    check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_passes_for_global_moderator_without_permission_for_other_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    moderators_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    moderators_group.can_select_own_thread_solutions = False
    moderators_group.save()

    solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(moderator)
    check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_passes_for_global_moderator_without_permission_for_deleted_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    moderators_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    moderators_group.can_select_own_thread_solutions = False
    moderators_group.save()

    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(moderator)
    check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_passes_for_category_moderator_without_permission_for_own_thread(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    members_group,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.can_select_own_thread_solutions = False
    members_group.save()

    thread = thread_factory(default_category, starter=category_moderator)
    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(category_moderator)
    check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_passes_for_category_moderator_without_permission_for_other_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    members_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.can_select_own_thread_solutions = False
    members_group.save()

    solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(category_moderator)
    check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_passes_for_category_moderator_without_permission_for_deleted_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    members_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.can_select_own_thread_solutions = False
    members_group.save()

    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(category_moderator)
    check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_fails_for_user_without_permission_for_own_thread(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    user,
    members_group,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.can_select_own_thread_solutions = False
    members_group.save()

    thread = thread_factory(default_category, starter=user)
    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_fails_for_user_without_permission_for_other_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    user,
    members_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.can_select_own_thread_solutions = False
    members_group.save()

    solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_fails_for_user_without_permission_for_deleted_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    user,
    members_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.can_select_own_thread_solutions = False
    members_group.save()

    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_fails_for_anonymous_user_without_permission_for_other_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    guests_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    guests_group.can_select_own_thread_solutions = False
    guests_group.save()

    solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_fails_for_anonymous_user_without_permission_for_deleted_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    guests_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    guests_group.can_select_own_thread_solutions = False
    guests_group.save()

    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_passes_for_global_moderator_for_own_thread_in_locked_category(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    thread = thread_factory(default_category, starter=moderator)
    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(moderator)
    check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_passes_for_global_moderator_for_other_user_thread_in_locked_category(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(moderator)
    check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_passes_for_global_moderator_for_deleted_user_thread_in_locked_category(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(moderator)
    check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_passes_for_category_moderator_for_own_thread_in_locked_category(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    thread = thread_factory(default_category, starter=category_moderator)
    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(category_moderator)
    check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_passes_for_category_moderator_for_other_user_thread_in_locked_category(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(category_moderator)
    check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_passes_for_category_moderator_for_deleted_user_thread_in_locked_category(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(category_moderator)
    check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_fails_for_user_for_own_thread_in_locked_category(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    thread = thread_factory(default_category, starter=user)

    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_fails_for_user_for_other_user_thread_in_locked_category(
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_fails_for_user_for_deleted_user_thread_in_locked_category(
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_fails_for_anonymous_user_for_other_user_thread_in_locked_category(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    guests_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    guests_group.can_select_own_thread_solutions = True
    guests_group.save()

    solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_fails_for_anonymous_user_for_deleted_user_thread_in_locked_category(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    guests_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    guests_group.can_select_own_thread_solutions = True
    guests_group.save()

    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_passes_for_global_moderator_for_own_locked_thread(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    thread = thread_factory(default_category, starter=moderator, is_locked=True)

    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(moderator)
    check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_passes_for_global_moderator_for_other_user_locked_thread(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    other_user_thread.is_locked = True
    other_user_thread.save()

    solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(moderator)
    check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_passes_for_global_moderator_for_deleted_user_locked_thread(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    thread.is_locked = True
    thread.save()

    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(moderator)
    check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_passes_for_category_moderator_for_own_locked_thread(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    thread = thread_factory(
        default_category, starter=category_moderator, is_locked=True
    )
    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(category_moderator)
    check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_passes_for_category_moderator_for_other_user_locked_thread(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    other_user_thread.is_locked = True
    other_user_thread.save()

    solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(category_moderator)
    check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_passes_for_category_moderator_for_deleted_user_locked_thread(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    thread.is_locked = True
    thread.save()

    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(category_moderator)
    check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_fails_for_user_for_own_locked_thread(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    thread = thread_factory(default_category, starter=user, is_locked=True)
    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_fails_for_user_for_other_user_locked_thread(
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    other_user_thread.is_locked = True
    other_user_thread.save()

    solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_fails_for_user_for_deleted_user_locked_thread(
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    thread.is_locked = True
    thread.save()

    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_fails_for_anonymous_user_for_other_user_locked_thread(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    guests_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    other_user_thread.is_locked = True
    other_user_thread.save()

    guests_group.can_select_own_thread_solutions = True
    guests_group.save()

    solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_select_thread_solution_permission(permissions, solution)


def test_check_select_thread_solution_permission_fails_for_anonymous_user_for_deleted_user_locked_thread(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    guests_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    thread.is_locked = True
    thread.save()

    guests_group.can_select_own_thread_solutions = True
    guests_group.save()

    solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_select_thread_solution_permission(permissions, solution)


def test_check_change_thread_solution_permission_passes_for_global_moderator_for_own_thread_in_category_with_disabled_solutions(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
):
    default_category.enable_solutions = False
    default_category.save()

    thread = thread_factory(default_category, starter=moderator)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, moderator)

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_global_moderator_for_other_user_thread_in_category_with_disabled_solutions(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    other_user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = False
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_global_moderator_for_deleted_user_thread_in_category_with_disabled_solutions(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
    thread,
):
    default_category.enable_solutions = False
    default_category.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_category_moderator_for_own_thread_in_category_with_disabled_solutions(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
):
    default_category.enable_solutions = False
    default_category.save()

    thread = thread_factory(default_category, starter=category_moderator)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, category_moderator)

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(category_moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_category_moderator_for_other_user_thread_in_category_with_disabled_solutions(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    other_user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = False
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(category_moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_category_moderator_for_deleted_user_thread_in_category_with_disabled_solutions(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
    thread,
):
    default_category.enable_solutions = False
    default_category.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(category_moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_user_for_own_thread_in_category_with_disabled_solutions(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
):
    default_category.enable_solutions = False
    default_category.save()

    thread = thread_factory(default_category, starter=user)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, user)

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_user_for_other_user_thread_in_category_with_disabled_solutions(
    thread_reply_factory,
    user_permissions_factory,
    user,
    other_user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = False
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_user_for_deleted_user_thread_in_category_with_disabled_solutions(
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
    thread,
):
    default_category.enable_solutions = False
    default_category.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_anonymous_user_for_other_user_thread_in_category_with_disabled_solutions(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    other_user,
    guests_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = False
    default_category.save()

    guests_group.can_change_own_thread_solutions = True
    guests_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_anonymous_user_for_deleted_user_thread_in_category_with_disabled_solutions(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    guests_group,
    default_category,
    thread,
):
    default_category.enable_solutions = False
    default_category.save()

    guests_group.can_change_own_thread_solutions = True
    guests_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_global_moderator_for_own_thread(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    thread = thread_factory(default_category, starter=moderator)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, moderator)

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_global_moderator_for_other_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    other_user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_global_moderator_for_deleted_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_category_moderator_for_own_thread(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    thread = thread_factory(default_category, starter=category_moderator)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, category_moderator)

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(category_moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_category_moderator_for_other_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    other_user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(category_moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_category_moderator_for_deleted_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(category_moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_user_for_own_thread(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    thread = thread_factory(default_category, starter=user)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, user)

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(user)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_user_for_other_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    user,
    other_user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_user_for_deleted_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_anonymous_user_for_other_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    other_user,
    guests_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    guests_group.can_change_own_thread_solutions = True
    guests_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_anonymous_user_for_deleted_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    guests_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    guests_group.can_change_own_thread_solutions = True
    guests_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_global_moderator_without_permission_for_own_thread(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    moderators_group,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    moderators_group.can_change_own_thread_solutions = False
    moderators_group.save()

    thread = thread_factory(default_category, starter=moderator)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, moderator)

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_global_moderator_without_permission_for_other_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    other_user,
    moderators_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    moderators_group.can_change_own_thread_solutions = False
    moderators_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_global_moderator_without_permission_for_deleted_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    moderators_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    moderators_group.can_change_own_thread_solutions = False
    moderators_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_category_moderator_without_permission_for_own_thread(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    members_group,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.can_change_own_thread_solutions = False
    members_group.save()

    thread = thread_factory(default_category, starter=category_moderator)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, category_moderator)

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(category_moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_category_moderator_without_permission_for_other_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    other_user,
    members_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.can_change_own_thread_solutions = False
    members_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(category_moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_category_moderator_without_permission_for_deleted_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    members_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.can_change_own_thread_solutions = False
    members_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(category_moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_user_without_permission_for_own_thread(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    user,
    members_group,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.can_change_own_thread_solutions = False
    members_group.save()

    thread = thread_factory(default_category, starter=user)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, user)

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_user_without_permission_for_other_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    user,
    other_user,
    members_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.can_change_own_thread_solutions = False
    members_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_user_without_permission_for_deleted_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    user,
    members_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.can_change_own_thread_solutions = False
    members_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_anonymous_user_without_permission_for_other_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    other_user,
    guests_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    guests_group.can_change_own_thread_solutions = False
    guests_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_anonymous_user_without_permission_for_deleted_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    guests_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    guests_group.can_change_own_thread_solutions = False
    guests_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_global_moderator_for_own_thread_in_locked_category(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    thread = thread_factory(default_category, starter=moderator)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, moderator)

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_global_moderator_for_other_user_thread_in_locked_category(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    other_user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_global_moderator_for_deleted_user_thread_in_locked_category(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_category_moderator_for_own_thread_in_locked_category(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    thread = thread_factory(default_category, starter=category_moderator)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, category_moderator)

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(category_moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_category_moderator_for_other_user_thread_in_locked_category(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    other_user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(category_moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_category_moderator_for_deleted_user_thread_in_locked_category(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(category_moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_user_for_own_thread_in_locked_category(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    thread = thread_factory(default_category, starter=user)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, user)

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_user_for_other_user_thread_in_locked_category(
    thread_reply_factory,
    user_permissions_factory,
    user,
    other_user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_user_for_deleted_user_thread_in_locked_category(
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_anonymous_user_for_other_user_thread_in_locked_category(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    other_user,
    guests_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    guests_group.can_change_own_thread_solutions = True
    guests_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_anonymous_user_for_deleted_user_thread_in_locked_category(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    guests_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    guests_group.can_change_own_thread_solutions = True
    guests_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_global_moderator_for_own_locked_thread(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    thread = thread_factory(default_category, starter=moderator, is_locked=True)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, moderator)

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_global_moderator_for_other_user_locked_thread(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    other_user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    other_user_thread.is_locked = True
    other_user_thread.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_global_moderator_for_deleted_user_locked_thread(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    thread.is_locked = True
    thread.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_category_moderator_for_own_locked_thread(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    thread = thread_factory(
        default_category, starter=category_moderator, is_locked=True
    )
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, category_moderator)

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(category_moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_category_moderator_for_other_user_locked_thread(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    other_user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    other_user_thread.is_locked = True
    other_user_thread.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(category_moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_category_moderator_for_deleted_user_locked_thread(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    thread.is_locked = True
    thread.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(category_moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_user_for_own_locked_thread(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    thread = thread_factory(default_category, starter=user, is_locked=True)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, user)

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_user_for_other_user_locked_thread(
    thread_reply_factory,
    user_permissions_factory,
    user,
    other_user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    other_user_thread.is_locked = True
    other_user_thread.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_user_for_deleted_user_locked_thread(
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    thread.is_locked = True
    thread.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_anonymous_user_for_other_user_locked_thread(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    other_user,
    guests_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    other_user_thread.is_locked = True
    other_user_thread.save()

    guests_group.can_change_own_thread_solutions = True
    guests_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_anonymous_user_for_deleted_user_locked_thread(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    guests_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    thread.is_locked = True
    thread.save()

    guests_group.can_change_own_thread_solutions = True
    guests_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_global_moderator_for_own_thread_with_locked_solution(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    thread = thread_factory(default_category, starter=moderator)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, moderator)
    lock_thread_solution(thread, "Moderator")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_global_moderator_for_other_user_thread_with_locked_solution(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    other_user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)
    lock_thread_solution(other_user_thread, "Moderator")

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_global_moderator_for_deleted_user_thread_with_locked_solution(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")
    lock_thread_solution(thread, "Moderator")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_category_moderator_for_own_thread_with_locked_solution(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    thread = thread_factory(default_category, starter=category_moderator)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, category_moderator)
    lock_thread_solution(thread, "Moderator")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(category_moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_category_moderator_for_other_user_thread_with_locked_solution(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    other_user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)
    lock_thread_solution(other_user_thread, "Moderator")

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(category_moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_category_moderator_for_deleted_user_thread_with_locked_solution(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")
    lock_thread_solution(thread, "Moderator")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(category_moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_user_for_own_thread_with_locked_solution(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    thread = thread_factory(default_category, starter=user)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, user)
    lock_thread_solution(thread, "Moderator")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_user_for_other_user_thread_with_locked_solution(
    thread_reply_factory,
    user_permissions_factory,
    user,
    other_user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)
    lock_thread_solution(other_user_thread, "Moderator")

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_user_for_deleted_user_thread_with_locked_solution(
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")
    lock_thread_solution(thread, "Moderator")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_anonymous_user_for_other_user_thread_with_locked_solution(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    other_user,
    guests_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    guests_group.can_change_own_thread_solutions = True
    guests_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)
    lock_thread_solution(other_user_thread, "Moderator")

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_anonymous_user_for_deleted_user_thread_with_locked_solution(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    guests_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    guests_group.can_change_own_thread_solutions = True
    guests_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")
    lock_thread_solution(thread, "Moderator")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_global_moderator_for_own_thread_within_time_limit(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    moderators_group,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    moderators_group.own_thread_solutions_change_time_limit = 5
    moderators_group.save()

    thread = thread_factory(default_category, starter=moderator)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, moderator)

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_global_moderator_for_other_user_thread_within_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    other_user,
    moderators_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    moderators_group.own_thread_solutions_change_time_limit = 5
    moderators_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_global_moderator_for_deleted_user_thread_within_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    moderators_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    moderators_group.own_thread_solutions_change_time_limit = 5
    moderators_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_category_moderator_for_own_thread_within_time_limit(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    members_group,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.own_thread_solutions_change_time_limit = 5
    members_group.save()

    thread = thread_factory(default_category, starter=category_moderator)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, category_moderator)

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(category_moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_category_moderator_for_other_user_thread_within_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    other_user,
    members_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.own_thread_solutions_change_time_limit = 5
    members_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(category_moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_category_moderator_for_deleted_user_thread_within_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    members_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.own_thread_solutions_change_time_limit = 5
    members_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(category_moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_user_for_own_thread_within_time_limit(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    user,
    members_group,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.own_thread_solutions_change_time_limit = 5
    members_group.save()

    thread = thread_factory(default_category, starter=user)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, user)

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(user)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_user_for_other_user_thread_within_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    user,
    other_user,
    members_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.own_thread_solutions_change_time_limit = 5
    members_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_user_for_deleted_user_thread_within_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    user,
    members_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.own_thread_solutions_change_time_limit = 5
    members_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_anonymous_user_for_other_user_thread_within_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    other_user,
    guests_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    guests_group.can_change_own_thread_solutions = True
    guests_group.own_thread_solutions_change_time_limit = 5
    guests_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_anonymous_user_for_deleted_user_thread_within_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    guests_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    guests_group.can_change_own_thread_solutions = True
    guests_group.own_thread_solutions_change_time_limit = 5
    guests_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_global_moderator_for_own_thread_outside_of_time_limit(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    moderators_group,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    moderators_group.own_thread_solutions_change_time_limit = 5
    moderators_group.save()

    thread = thread_factory(default_category, starter=moderator)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, moderator)

    thread.solution_selected_at -= timedelta(minutes=30)
    thread.save()

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_global_moderator_for_other_user_thread_outside_of_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    other_user,
    moderators_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    moderators_group.own_thread_solutions_change_time_limit = 5
    moderators_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    other_user_thread.solution_selected_at -= timedelta(minutes=30)
    other_user_thread.save()

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_global_moderator_for_deleted_user_thread_outside_of_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    moderators_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    moderators_group.own_thread_solutions_change_time_limit = 5
    moderators_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    thread.solution_selected_at -= timedelta(minutes=30)
    thread.save()

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_category_moderator_for_own_thread_outside_of_time_limit(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    members_group,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.own_thread_solutions_change_time_limit = 5
    members_group.save()

    thread = thread_factory(default_category, starter=category_moderator)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, category_moderator)

    thread.solution_selected_at -= timedelta(minutes=30)
    thread.save()

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(category_moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_category_moderator_for_other_user_thread_outside_of_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    other_user,
    members_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.own_thread_solutions_change_time_limit = 5
    members_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    other_user_thread.solution_selected_at -= timedelta(minutes=30)
    other_user_thread.save()

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(category_moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_passes_for_category_moderator_for_deleted_user_thread_outside_of_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    members_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.own_thread_solutions_change_time_limit = 5
    members_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    thread.solution_selected_at -= timedelta(minutes=30)
    thread.save()

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(category_moderator)
    check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_user_for_own_thread_outside_of_time_limit(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    user,
    members_group,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.own_thread_solutions_change_time_limit = 5
    members_group.save()

    thread = thread_factory(default_category, starter=user)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, user)

    thread.solution_selected_at -= timedelta(minutes=30)
    thread.save()

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_user_for_other_user_thread_outside_of_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    user,
    other_user,
    members_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.own_thread_solutions_change_time_limit = 5
    members_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    other_user_thread.solution_selected_at -= timedelta(minutes=30)
    other_user_thread.save()

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_user_for_deleted_user_thread_outside_of_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    user,
    members_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.own_thread_solutions_change_time_limit = 5
    members_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    thread.solution_selected_at -= timedelta(minutes=30)
    thread.save()

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_anonymous_user_for_other_user_thread_outside_of_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    other_user,
    guests_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    guests_group.can_change_own_thread_solutions = True
    guests_group.own_thread_solutions_change_time_limit = 5
    guests_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    other_user_thread.solution_selected_at -= timedelta(minutes=30)
    other_user_thread.save()

    new_solution = thread_reply_factory(other_user_thread)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_change_thread_solution_permission_fails_for_anonymous_user_for_deleted_user_thread_outside_of_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    guests_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    guests_group.can_change_own_thread_solutions = True
    guests_group.own_thread_solutions_change_time_limit = 5
    guests_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    thread.solution_selected_at -= timedelta(minutes=30)
    thread.save()

    new_solution = thread_reply_factory(thread)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_change_thread_solution_permission(permissions, new_solution)


def test_check_clear_thread_solution_permission_passes_for_global_moderator_for_own_thread_in_category_with_disabled_solutions(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
):
    default_category.enable_solutions = False
    default_category.save()

    thread = thread_factory(default_category, starter=moderator)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, moderator)

    permissions = user_permissions_factory(moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_global_moderator_for_other_user_thread_in_category_with_disabled_solutions(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    other_user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = False
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    permissions = user_permissions_factory(moderator)
    check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_passes_for_global_moderator_for_deleted_user_thread_in_category_with_disabled_solutions(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
    thread,
):
    default_category.enable_solutions = False
    default_category.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    permissions = user_permissions_factory(moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_category_moderator_for_own_thread_in_category_with_disabled_solutions(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
):
    default_category.enable_solutions = False
    default_category.save()

    thread = thread_factory(default_category, starter=category_moderator)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, category_moderator)

    permissions = user_permissions_factory(category_moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_category_moderator_for_other_user_thread_in_category_with_disabled_solutions(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    other_user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = False
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    permissions = user_permissions_factory(category_moderator)
    check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_passes_for_category_moderator_for_deleted_user_thread_in_category_with_disabled_solutions(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
    thread,
):
    default_category.enable_solutions = False
    default_category.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    permissions = user_permissions_factory(category_moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_fails_for_user_for_own_thread_in_category_with_disabled_solutions(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
):
    default_category.enable_solutions = False
    default_category.save()

    thread = thread_factory(default_category, starter=user)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, user)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_fails_for_user_for_other_user_thread_in_category_with_disabled_solutions(
    thread_reply_factory,
    user_permissions_factory,
    user,
    other_user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = False
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_fails_for_user_for_deleted_user_thread_in_category_with_disabled_solutions(
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
    thread,
):
    default_category.enable_solutions = False
    default_category.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_fails_for_anonymous_user_for_other_user_thread_in_category_with_disabled_solutions(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    other_user,
    guests_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = False
    default_category.save()

    guests_group.can_clear_own_thread_solutions = True
    guests_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_fails_for_anonymous_user_for_deleted_user_thread_in_category_with_disabled_solutions(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    guests_group,
    default_category,
    thread,
):
    default_category.enable_solutions = False
    default_category.save()

    guests_group.can_clear_own_thread_solutions = True
    guests_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_global_moderator_for_own_thread(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    thread = thread_factory(default_category, starter=moderator)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, moderator)

    permissions = user_permissions_factory(moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_global_moderator_for_other_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    other_user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    permissions = user_permissions_factory(moderator)
    check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_passes_for_global_moderator_for_deleted_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    permissions = user_permissions_factory(moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_category_moderator_for_own_thread(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    thread = thread_factory(default_category, starter=category_moderator)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, category_moderator)

    permissions = user_permissions_factory(category_moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_category_moderator_for_other_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    other_user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    permissions = user_permissions_factory(category_moderator)
    check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_passes_for_category_moderator_for_deleted_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    permissions = user_permissions_factory(category_moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_user_for_own_thread(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    thread = thread_factory(default_category, starter=user)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, user)

    permissions = user_permissions_factory(user)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_fails_for_user_for_other_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    user,
    other_user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_fails_for_user_for_deleted_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_fails_for_anonymous_user_for_other_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    other_user,
    guests_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    guests_group.can_clear_own_thread_solutions = True
    guests_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_fails_for_anonymous_user_for_deleted_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    guests_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    guests_group.can_clear_own_thread_solutions = True
    guests_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_global_moderator_without_permission_for_own_thread(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    moderators_group,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    moderators_group.can_clear_own_thread_solutions = False
    moderators_group.save()

    thread = thread_factory(default_category, starter=moderator)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, moderator)

    permissions = user_permissions_factory(moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_global_moderator_without_permission_for_other_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    other_user,
    moderators_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    moderators_group.can_clear_own_thread_solutions = False
    moderators_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    permissions = user_permissions_factory(moderator)
    check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_passes_for_global_moderator_without_permission_for_deleted_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    moderators_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    moderators_group.can_clear_own_thread_solutions = False
    moderators_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    permissions = user_permissions_factory(moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_category_moderator_without_permission_for_own_thread(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    members_group,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.can_clear_own_thread_solutions = False
    members_group.save()

    thread = thread_factory(default_category, starter=category_moderator)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, category_moderator)

    permissions = user_permissions_factory(category_moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_category_moderator_without_permission_for_other_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    other_user,
    members_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.can_clear_own_thread_solutions = False
    members_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    permissions = user_permissions_factory(category_moderator)
    check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_passes_for_category_moderator_without_permission_for_deleted_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    members_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.can_clear_own_thread_solutions = False
    members_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    permissions = user_permissions_factory(category_moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_fails_for_user_without_permission_for_own_thread(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    user,
    members_group,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.can_clear_own_thread_solutions = False
    members_group.save()

    thread = thread_factory(default_category, starter=user)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, user)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_fails_for_user_without_permission_for_other_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    user,
    other_user,
    members_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.can_clear_own_thread_solutions = False
    members_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_fails_for_user_without_permission_for_deleted_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    user,
    members_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.can_clear_own_thread_solutions = False
    members_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_fails_for_anonymous_user_without_permission_for_other_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    other_user,
    guests_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    guests_group.can_clear_own_thread_solutions = False
    guests_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_fails_for_anonymous_user_without_permission_for_deleted_user_thread(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    guests_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    guests_group.can_clear_own_thread_solutions = False
    guests_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_global_moderator_for_own_thread_in_locked_category(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    thread = thread_factory(default_category, starter=moderator)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, moderator)

    permissions = user_permissions_factory(moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_global_moderator_for_other_user_thread_in_locked_category(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    other_user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    permissions = user_permissions_factory(moderator)
    check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_passes_for_global_moderator_for_deleted_user_thread_in_locked_category(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    permissions = user_permissions_factory(moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_category_moderator_for_own_thread_in_locked_category(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    thread = thread_factory(default_category, starter=category_moderator)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, category_moderator)

    permissions = user_permissions_factory(category_moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_category_moderator_for_other_user_thread_in_locked_category(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    other_user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    permissions = user_permissions_factory(category_moderator)
    check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_passes_for_category_moderator_for_deleted_user_thread_in_locked_category(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    permissions = user_permissions_factory(category_moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_fails_for_user_for_own_thread_in_locked_category(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    thread = thread_factory(default_category, starter=user)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, user)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_fails_for_user_for_other_user_thread_in_locked_category(
    thread_reply_factory,
    user_permissions_factory,
    user,
    other_user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_fails_for_user_for_deleted_user_thread_in_locked_category(
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_fails_for_anonymous_user_for_other_user_thread_in_locked_category(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    other_user,
    guests_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    guests_group.can_clear_own_thread_solutions = True
    guests_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_fails_for_anonymous_user_for_deleted_user_thread_in_locked_category(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    guests_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.is_locked = True
    default_category.save()

    guests_group.can_clear_own_thread_solutions = True
    guests_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_global_moderator_for_own_locked_thread(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    thread = thread_factory(default_category, starter=moderator, is_locked=True)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, moderator)

    permissions = user_permissions_factory(moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_global_moderator_for_other_user_locked_thread(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    other_user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    other_user_thread.is_locked = True
    other_user_thread.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    permissions = user_permissions_factory(moderator)
    check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_passes_for_global_moderator_for_deleted_user_locked_thread(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    thread.is_locked = True
    thread.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    permissions = user_permissions_factory(moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_category_moderator_for_own_locked_thread(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    thread = thread_factory(
        default_category, starter=category_moderator, is_locked=True
    )
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, category_moderator)

    permissions = user_permissions_factory(category_moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_category_moderator_for_other_user_locked_thread(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    other_user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    other_user_thread.is_locked = True
    other_user_thread.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    permissions = user_permissions_factory(category_moderator)
    check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_passes_for_category_moderator_for_deleted_user_locked_thread(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    thread.is_locked = True
    thread.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    permissions = user_permissions_factory(category_moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_fails_for_user_for_own_locked_thread(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    thread = thread_factory(default_category, starter=user, is_locked=True)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, user)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_fails_for_user_for_other_user_locked_thread(
    thread_reply_factory,
    user_permissions_factory,
    user,
    other_user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    other_user_thread.is_locked = True
    other_user_thread.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_fails_for_user_for_deleted_user_locked_thread(
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    thread.is_locked = True
    thread.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_fails_for_anonymous_user_for_other_user_locked_thread(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    other_user,
    guests_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    other_user_thread.is_locked = True
    other_user_thread.save()

    guests_group.can_clear_own_thread_solutions = True
    guests_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_fails_for_anonymous_user_for_deleted_user_locked_thread(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    guests_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    thread.is_locked = True
    thread.save()

    guests_group.can_clear_own_thread_solutions = True
    guests_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_global_moderator_for_own_thread_with_locked_solution(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    thread = thread_factory(default_category, starter=moderator)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, moderator)
    lock_thread_solution(thread, "Moderator")

    permissions = user_permissions_factory(moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_global_moderator_for_other_user_thread_with_locked_solution(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    other_user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)
    lock_thread_solution(other_user_thread, "Moderator")

    permissions = user_permissions_factory(moderator)
    check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_passes_for_global_moderator_for_deleted_user_thread_with_locked_solution(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")
    lock_thread_solution(thread, "Moderator")

    permissions = user_permissions_factory(moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_category_moderator_for_own_thread_with_locked_solution(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    thread = thread_factory(default_category, starter=category_moderator)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, category_moderator)
    lock_thread_solution(thread, "Moderator")

    permissions = user_permissions_factory(category_moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_category_moderator_for_other_user_thread_with_locked_solution(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    other_user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)
    lock_thread_solution(other_user_thread, "Moderator")

    permissions = user_permissions_factory(category_moderator)
    check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_passes_for_category_moderator_for_deleted_user_thread_with_locked_solution(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")
    lock_thread_solution(thread, "Moderator")

    permissions = user_permissions_factory(category_moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_fails_for_user_for_own_thread_with_locked_solution(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    thread = thread_factory(default_category, starter=user)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, user)
    lock_thread_solution(thread, "Moderator")

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_fails_for_user_for_other_user_thread_with_locked_solution(
    thread_reply_factory,
    user_permissions_factory,
    user,
    other_user,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)
    lock_thread_solution(other_user_thread, "Moderator")

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_fails_for_user_for_deleted_user_thread_with_locked_solution(
    thread_reply_factory,
    user_permissions_factory,
    user,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")
    lock_thread_solution(thread, "Moderator")

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_fails_for_anonymous_user_for_other_user_thread_with_locked_solution(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    other_user,
    guests_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    guests_group.can_clear_own_thread_solutions = True
    guests_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)
    lock_thread_solution(other_user_thread, "Moderator")

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_fails_for_anonymous_user_for_deleted_user_thread_with_locked_solution(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    guests_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    guests_group.can_clear_own_thread_solutions = True
    guests_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")
    lock_thread_solution(thread, "Moderator")

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_global_moderator_for_own_thread_within_time_limit(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    moderators_group,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    moderators_group.own_thread_solutions_clear_time_limit = 5
    moderators_group.save()

    thread = thread_factory(default_category, starter=moderator)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, moderator)

    permissions = user_permissions_factory(moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_global_moderator_for_other_user_thread_within_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    other_user,
    moderators_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    moderators_group.own_thread_solutions_clear_time_limit = 5
    moderators_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    permissions = user_permissions_factory(moderator)
    check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_passes_for_global_moderator_for_deleted_user_thread_within_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    moderators_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    moderators_group.own_thread_solutions_clear_time_limit = 5
    moderators_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    permissions = user_permissions_factory(moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_category_moderator_for_own_thread_within_time_limit(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    members_group,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.own_thread_solutions_clear_time_limit = 5
    members_group.save()

    thread = thread_factory(default_category, starter=category_moderator)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, category_moderator)

    permissions = user_permissions_factory(category_moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_category_moderator_for_other_user_thread_within_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    other_user,
    members_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.own_thread_solutions_clear_time_limit = 5
    members_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    permissions = user_permissions_factory(category_moderator)
    check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_passes_for_category_moderator_for_deleted_user_thread_within_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    members_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.own_thread_solutions_clear_time_limit = 5
    members_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    permissions = user_permissions_factory(category_moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_user_for_own_thread_within_time_limit(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    user,
    members_group,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.own_thread_solutions_clear_time_limit = 5
    members_group.save()

    thread = thread_factory(default_category, starter=user)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, user)

    permissions = user_permissions_factory(user)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_fails_for_user_for_other_user_thread_within_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    user,
    other_user,
    members_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.own_thread_solutions_clear_time_limit = 5
    members_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_fails_for_user_for_deleted_user_thread_within_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    user,
    members_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.own_thread_solutions_clear_time_limit = 5
    members_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_fails_for_anonymous_user_for_other_user_thread_within_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    other_user,
    guests_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    guests_group.can_clear_own_thread_solutions = True
    guests_group.own_thread_solutions_clear_time_limit = 5
    guests_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_fails_for_anonymous_user_for_deleted_user_thread_within_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    guests_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    guests_group.can_clear_own_thread_solutions = True
    guests_group.own_thread_solutions_clear_time_limit = 5
    guests_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_global_moderator_for_own_thread_outside_of_time_limit(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    moderators_group,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    moderators_group.own_thread_solutions_clear_time_limit = 5
    moderators_group.save()

    thread = thread_factory(default_category, starter=moderator)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, moderator)

    thread.solution_selected_at -= timedelta(minutes=30)
    thread.save()

    permissions = user_permissions_factory(moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_global_moderator_for_other_user_thread_outside_of_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    other_user,
    moderators_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    moderators_group.own_thread_solutions_clear_time_limit = 5
    moderators_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    other_user_thread.solution_selected_at -= timedelta(minutes=30)
    other_user_thread.save()

    permissions = user_permissions_factory(moderator)
    check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_passes_for_global_moderator_for_deleted_user_thread_outside_of_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    moderator,
    moderators_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    moderators_group.own_thread_solutions_clear_time_limit = 5
    moderators_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    thread.solution_selected_at -= timedelta(minutes=30)
    thread.save()

    permissions = user_permissions_factory(moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_category_moderator_for_own_thread_outside_of_time_limit(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    members_group,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.own_thread_solutions_clear_time_limit = 5
    members_group.save()

    thread = thread_factory(default_category, starter=category_moderator)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, category_moderator)

    thread.solution_selected_at -= timedelta(minutes=30)
    thread.save()

    permissions = user_permissions_factory(category_moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_passes_for_category_moderator_for_other_user_thread_outside_of_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    other_user,
    members_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.own_thread_solutions_clear_time_limit = 5
    members_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    other_user_thread.solution_selected_at -= timedelta(minutes=30)
    other_user_thread.save()

    permissions = user_permissions_factory(category_moderator)
    check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_passes_for_category_moderator_for_deleted_user_thread_outside_of_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    category_moderator,
    members_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.own_thread_solutions_clear_time_limit = 5
    members_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    thread.solution_selected_at -= timedelta(minutes=30)
    thread.save()

    permissions = user_permissions_factory(category_moderator)
    check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_fails_for_user_for_own_thread_outside_of_time_limit(
    thread_factory,
    thread_reply_factory,
    user_permissions_factory,
    user,
    members_group,
    default_category,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.own_thread_solutions_clear_time_limit = 5
    members_group.save()

    thread = thread_factory(default_category, starter=user)
    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, user)

    thread.solution_selected_at -= timedelta(minutes=30)
    thread.save()

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_fails_for_user_for_other_user_thread_outside_of_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    user,
    other_user,
    members_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.own_thread_solutions_clear_time_limit = 5
    members_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    other_user_thread.solution_selected_at -= timedelta(minutes=30)
    other_user_thread.save()

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_fails_for_user_for_deleted_user_thread_outside_of_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    user,
    members_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    members_group.own_thread_solutions_clear_time_limit = 5
    members_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    thread.solution_selected_at -= timedelta(minutes=30)
    thread.save()

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, thread)


def test_check_clear_thread_solution_permission_fails_for_anonymous_user_for_other_user_thread_outside_of_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    other_user,
    guests_group,
    default_category,
    other_user_thread,
):
    default_category.enable_solutions = True
    default_category.save()

    guests_group.can_clear_own_thread_solutions = True
    guests_group.own_thread_solutions_clear_time_limit = 5
    guests_group.save()

    solution = thread_reply_factory(other_user_thread)

    select_thread_solution(other_user_thread, solution, other_user)

    other_user_thread.solution_selected_at -= timedelta(minutes=30)
    other_user_thread.save()

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, other_user_thread)


def test_check_clear_thread_solution_permission_fails_for_anonymous_user_for_deleted_user_thread_outside_of_time_limit(
    thread_reply_factory,
    user_permissions_factory,
    anonymous_user,
    guests_group,
    default_category,
    thread,
):
    default_category.enable_solutions = True
    default_category.save()

    guests_group.can_clear_own_thread_solutions = True
    guests_group.own_thread_solutions_clear_time_limit = 5
    guests_group.save()

    solution = thread_reply_factory(thread)

    select_thread_solution(thread, solution, "DeletedUser")

    thread.solution_selected_at -= timedelta(minutes=30)
    thread.save()

    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_clear_thread_solution_permission(permissions, thread)


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
