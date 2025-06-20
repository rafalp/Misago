import pytest
from django.core.exceptions import PermissionDenied

from ..models import Moderator
from ..threads import (
    check_close_thread_poll_permission,
    check_edit_thread_poll_permission,
    check_start_thread_poll_permission,
)


def test_check_start_thread_poll_permission_passes_if_user_has_permission(
    user, user_permissions_factory, default_category, user_thread
):
    permissions = user_permissions_factory(user)
    check_start_thread_poll_permission(permissions, default_category, user_thread)


def test_check_start_thread_poll_permission_fails_if_user_is_anonymous(
    anonymous_user, user_permissions_factory, default_category, user_thread
):
    permissions = user_permissions_factory(anonymous_user)

    with pytest.raises(PermissionDenied):
        check_start_thread_poll_permission(permissions, default_category, user_thread)


def test_check_start_thread_poll_permission_fails_if_user_has_no_permission(
    user, members_group, user_permissions_factory, default_category, user_thread
):
    members_group.can_start_polls = False
    members_group.save()

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_start_thread_poll_permission(permissions, default_category, user_thread)


def test_check_start_thread_poll_permission_fails_if_user_is_not_thread_starter(
    user, user_permissions_factory, default_category, thread
):
    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_start_thread_poll_permission(permissions, default_category, thread)


def test_check_start_thread_poll_permission_passes_if_user_is_category_moderator(
    user, user_permissions_factory, default_category, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    permissions = user_permissions_factory(user)
    check_start_thread_poll_permission(permissions, default_category, thread)


def test_check_start_thread_poll_permission_passes_if_user_is_global_moderator(
    moderator, user_permissions_factory, default_category, user_thread
):
    permissions = user_permissions_factory(moderator)
    check_start_thread_poll_permission(permissions, default_category, user_thread)


def test_check_start_thread_poll_permission_fails_for_user_if_category_is_closed(
    user, user_permissions_factory, default_category, user_thread
):
    default_category.is_closed = True
    default_category.save()

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_start_thread_poll_permission(permissions, default_category, user_thread)


def test_check_start_thread_poll_permission_passes_for_category_moderator_if_category_is_closed(
    user, user_permissions_factory, default_category, user_thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    default_category.is_closed = True
    default_category.save()

    permissions = user_permissions_factory(user)
    check_start_thread_poll_permission(permissions, default_category, user_thread)


def test_check_start_thread_poll_permission_passes_for_global_moderator_if_category_is_closed(
    moderator, user_permissions_factory, default_category, user_thread
):
    default_category.is_closed = True
    default_category.save()

    permissions = user_permissions_factory(moderator)
    check_start_thread_poll_permission(permissions, default_category, user_thread)


def test_check_start_thread_poll_permission_fails_for_user_if_thread_is_closed(
    user, user_permissions_factory, default_category, user_thread
):
    user_thread.is_closed = True
    user_thread.save()

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_start_thread_poll_permission(permissions, default_category, user_thread)


def test_check_start_thread_poll_permission_passes_for_category_moderator_if_thread_is_closed(
    user, user_permissions_factory, default_category, user_thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    user_thread.is_closed = True
    user_thread.save()

    permissions = user_permissions_factory(user)
    check_start_thread_poll_permission(permissions, default_category, user_thread)


def test_check_start_thread_poll_permission_passes_for_global_moderator_if_thread_is_closed(
    moderator, user_permissions_factory, default_category, user_thread
):
    user_thread.is_closed = True
    user_thread.save()

    permissions = user_permissions_factory(moderator)
    check_start_thread_poll_permission(permissions, default_category, user_thread)


def test_check_edit_thread_poll_permission_passes_if_user_has_permission(
    user, user_permissions_factory, default_category, user_thread, user_poll
):
    permissions = user_permissions_factory(user)
    check_edit_thread_poll_permission(
        permissions, default_category, user_thread, user_poll
    )


def test_check_edit_thread_poll_permission_fails_if_user_has_no_permission(
    user,
    user_permissions_factory,
    members_group,
    default_category,
    user_thread,
    user_poll,
):
    members_group.can_edit_polls = False
    members_group.save()

    permissions = user_permissions_factory(user)
    check_edit_thread_poll_permission(
        permissions, default_category, user_thread, user_poll
    )
