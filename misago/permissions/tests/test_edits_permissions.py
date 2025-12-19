import pytest
from django.core.exceptions import PermissionDenied

from ..edits import can_see_post_edit_count, check_see_post_edit_history_permission
from ..enums import CanSeePostEdits


def test_can_see_post_edit_count_always_returns_true_if_user_is_post_owner(
    user, members_group, user_permissions_factory, default_category, thread, user_reply
):
    members_group.can_see_others_post_edits = CanSeePostEdits.NEVER
    members_group.save()

    permissions = user_permissions_factory(user)
    assert can_see_post_edit_count(permissions, default_category, thread, user_reply)


def test_can_see_post_edit_count_always_returns_true_if_user_has_count_permission(
    user, members_group, user_permissions_factory, default_category, thread, post
):
    members_group.can_see_others_post_edits = CanSeePostEdits.COUNT
    members_group.save()

    permissions = user_permissions_factory(user)
    assert can_see_post_edit_count(permissions, default_category, thread, post)


def test_can_see_post_edit_count_always_returns_true_if_user_has_history_permission(
    user, members_group, user_permissions_factory, default_category, thread, post
):
    members_group.can_see_others_post_edits = CanSeePostEdits.HISTORY
    members_group.save()

    permissions = user_permissions_factory(user)
    assert can_see_post_edit_count(permissions, default_category, thread, post)


def test_can_see_post_edit_count_always_returns_false_if_user_has_no_permission(
    user, members_group, user_permissions_factory, default_category, thread, post
):
    members_group.can_see_others_post_edits = CanSeePostEdits.NEVER
    members_group.save()

    permissions = user_permissions_factory(user)
    assert not can_see_post_edit_count(permissions, default_category, thread, post)


def test_check_see_post_edit_history_permission_always_passes_if_user_is_post_owner(
    user, members_group, user_permissions_factory, default_category, thread, user_reply
):
    members_group.can_see_others_post_edits = CanSeePostEdits.NEVER
    members_group.save()

    permissions = user_permissions_factory(user)
    check_see_post_edit_history_permission(
        permissions, default_category, thread, user_reply
    )


def test_check_see_post_edit_history_permission_passes_if_user_has_history_permission(
    user, members_group, user_permissions_factory, default_category, thread, post
):
    members_group.can_see_others_post_edits = CanSeePostEdits.HISTORY
    members_group.save()

    permissions = user_permissions_factory(user)
    check_see_post_edit_history_permission(permissions, default_category, thread, post)


def test_check_see_post_edit_history_permission_fails_if_user_has_count_permission(
    user, members_group, user_permissions_factory, default_category, thread, post
):
    members_group.can_see_others_post_edits = CanSeePostEdits.COUNT
    members_group.save()

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_see_post_edit_history_permission(
            permissions, default_category, thread, post
        )


def test_check_see_post_edit_history_permission_fails_if_user_has_no_permission(
    user, members_group, user_permissions_factory, default_category, thread, post
):
    members_group.can_see_others_post_edits = CanSeePostEdits.NEVER
    members_group.save()

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_see_post_edit_history_permission(
            permissions, default_category, thread, post
        )
