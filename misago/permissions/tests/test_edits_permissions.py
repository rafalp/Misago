from datetime import timedelta

import pytest
from django.core.exceptions import PermissionDenied

from ...edits.create import create_post_edit
from ...edits.hide import hide_post_edit
from ..edits import (
    can_see_post_edit_count,
    check_delete_post_edit_permission,
    check_hide_post_edit_permission,
    check_restore_post_edit_permission,
    check_see_post_edit_history_permission,
    check_unhide_post_edit_permission,
)
from ..enums import CanHideOwnPostEdits, CanSeePostEdits
from ..models import Moderator


def test_can_see_post_edit_count_always_returns_true_if_user_is_post_owner(
    user_permissions_factory, user, members_group, default_category, thread, user_reply
):
    members_group.can_see_others_post_edits = CanSeePostEdits.NEVER
    members_group.save()

    permissions = user_permissions_factory(user)
    assert can_see_post_edit_count(permissions, default_category, thread, user_reply)


def test_can_see_post_edit_count_always_returns_true_if_user_has_count_permission(
    user_permissions_factory, user, members_group, default_category, thread, post
):
    members_group.can_see_others_post_edits = CanSeePostEdits.COUNT
    members_group.save()

    permissions = user_permissions_factory(user)
    assert can_see_post_edit_count(permissions, default_category, thread, post)


def test_can_see_post_edit_count_always_returns_true_if_user_has_history_permission(
    user_permissions_factory, user, members_group, default_category, thread, post
):
    members_group.can_see_others_post_edits = CanSeePostEdits.HISTORY
    members_group.save()

    permissions = user_permissions_factory(user)
    assert can_see_post_edit_count(permissions, default_category, thread, post)


def test_can_see_post_edit_count_always_returns_false_if_user_has_no_permission(
    user_permissions_factory, user, members_group, default_category, thread, post
):
    members_group.can_see_others_post_edits = CanSeePostEdits.NEVER
    members_group.save()

    permissions = user_permissions_factory(user)
    assert not can_see_post_edit_count(permissions, default_category, thread, post)


def test_check_restore_post_edit_permission_passes_if_user_can_see_post_edit_contents(
    user_permissions_factory, user, user_reply
):
    post_edit = create_post_edit(
        post=user_reply, user=user, old_content="Lorem ipsum", new_content="Dolor met"
    )

    permissions = user_permissions_factory(user)
    check_restore_post_edit_permission(permissions, post_edit)


def test_check_restore_post_edit_permission_fails_if_user_cant_see_hidden_post_edit_contents(
    user_permissions_factory, user, user_reply
):
    post_edit = create_post_edit(
        post=user_reply, user=user, old_content="Lorem ipsum", new_content="Dolor met"
    )
    hide_post_edit(post_edit, "Moderator")

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_restore_post_edit_permission(permissions, post_edit)


def test_check_restore_post_edit_permission_passes_if_user_can_see_hidden_post_edit_contents(
    user_permissions_factory, moderator, user_reply
):
    post_edit = create_post_edit(
        post=user_reply,
        user=moderator,
        old_content="Lorem ipsum",
        new_content="Dolor met",
    )
    hide_post_edit(post_edit, "Moderator")

    permissions = user_permissions_factory(moderator)
    check_restore_post_edit_permission(permissions, post_edit)


def test_check_restore_post_edit_permission_fails_if_post_edit_has_no_contents(
    user_permissions_factory, user, user_reply
):
    post_edit = create_post_edit(post=user_reply, user=user)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_restore_post_edit_permission(permissions, post_edit)


def test_check_see_post_edit_history_permission_always_passes_if_user_is_post_owner(
    user_permissions_factory, user, members_group, default_category, thread, user_reply
):
    members_group.can_see_others_post_edits = CanSeePostEdits.NEVER
    members_group.save()

    permissions = user_permissions_factory(user)
    check_see_post_edit_history_permission(
        permissions, default_category, thread, user_reply
    )


def test_check_see_post_edit_history_permission_passes_if_user_has_history_permission(
    user_permissions_factory, user, members_group, default_category, thread, post
):
    members_group.can_see_others_post_edits = CanSeePostEdits.HISTORY
    members_group.save()

    permissions = user_permissions_factory(user)
    check_see_post_edit_history_permission(permissions, default_category, thread, post)


def test_check_see_post_edit_history_permission_fails_if_user_has_count_permission(
    user_permissions_factory, user, members_group, default_category, thread, post
):
    members_group.can_see_others_post_edits = CanSeePostEdits.COUNT
    members_group.save()

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_see_post_edit_history_permission(
            permissions, default_category, thread, post
        )


def test_check_see_post_edit_history_permission_fails_if_user_has_no_permission(
    user_permissions_factory, user, members_group, default_category, thread, post
):
    members_group.can_see_others_post_edits = CanSeePostEdits.NEVER
    members_group.save()

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_see_post_edit_history_permission(
            permissions, default_category, thread, post
        )


def test_check_hide_post_edit_permission_passes_for_thread_post_edit_for_global_moderator(
    user_permissions_factory, moderator, post
):
    post_edit = create_post_edit(post=post, user="DeletedUser")

    permissions = user_permissions_factory(moderator)
    check_hide_post_edit_permission(permissions, post_edit)


def test_check_hide_post_edit_permission_passes_for_thread_post_edit_for_category_moderator(
    user_permissions_factory, user, post
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[post.category_id],
    )

    post_edit = create_post_edit(post=post, user="DeletedUser")

    permissions = user_permissions_factory(user)
    check_hide_post_edit_permission(permissions, post_edit)


def test_check_hide_post_edit_permission_passes_for_private_thread_post_edit_for_global_moderator(
    user_permissions_factory, moderator, private_thread
):
    post = private_thread.first_post
    post_edit = create_post_edit(post=post, user="DeletedUser")

    permissions = user_permissions_factory(moderator)
    check_hide_post_edit_permission(permissions, post_edit)


def test_check_hide_post_edit_permission_passes_for_private_thread_post_edit_for_private_threads_moderator(
    user_permissions_factory, user, private_thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    post = private_thread.first_post
    post_edit = create_post_edit(post=post, user="DeletedUser")

    permissions = user_permissions_factory(user)
    check_hide_post_edit_permission(permissions, post_edit)


def test_check_hide_post_edit_permission_fails_user_for_deleted_user_post_edit(
    user_permissions_factory, user, post
):
    post_edit = create_post_edit(post=post, user="DeletedUser")

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_hide_post_edit_permission(permissions, post_edit)


def test_check_hide_post_edit_permission_fails_user_for_other_user_post_edit(
    user_permissions_factory, user, other_user, post
):
    post_edit = create_post_edit(post=post, user=other_user)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_hide_post_edit_permission(permissions, post_edit)


def test_check_hide_post_edit_permission_passes_user_with_hide_permission_for_own_post_edit(
    user_permissions_factory, user, members_group, post
):
    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.HIDE
    members_group.save()

    post_edit = create_post_edit(post=post, user=user)

    permissions = user_permissions_factory(user)
    check_hide_post_edit_permission(permissions, post_edit)


def test_check_hide_post_edit_permission_fails_user_without_hide_permission_for_own_post_edit(
    user_permissions_factory, user, members_group, post
):
    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.NEVER
    members_group.save()

    post_edit = create_post_edit(post=post, user=user)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_hide_post_edit_permission(permissions, post_edit)


def test_check_hide_post_edit_permission_passes_user_with_delete_permission_for_own_post_edit(
    user_permissions_factory, user, members_group, post
):
    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    post_edit = create_post_edit(post=post, user=user)

    permissions = user_permissions_factory(user)
    check_hide_post_edit_permission(permissions, post_edit)


def test_check_hide_post_edit_permission_passes_user_with_hide_permission_for_own_post_edit_if_its_within_time_limit(
    user_permissions_factory, user, members_group, post
):
    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.own_post_edits_hide_time_limit = 90
    members_group.save()

    post_edit = create_post_edit(post=post, user=user)
    post_edit.edited_at -= timedelta(minutes=30)

    permissions = user_permissions_factory(user)
    check_hide_post_edit_permission(permissions, post_edit)


def test_check_hide_post_edit_permission_fails_user_with_hide_permission_for_own_post_edit_if_its_too_old(
    user_permissions_factory, user, members_group, post
):
    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.own_post_edits_hide_time_limit = 30
    members_group.save()

    post_edit = create_post_edit(post=post, user=user)
    post_edit.edited_at -= timedelta(hours=6)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_hide_post_edit_permission(permissions, post_edit)


def test_check_unhide_post_edit_permission_passes_for_thread_post_edit_for_global_moderator(
    user_permissions_factory, moderator, post
):
    post_edit = create_post_edit(post=post, user="DeletedUser")

    permissions = user_permissions_factory(moderator)
    check_unhide_post_edit_permission(permissions, post_edit)


def test_check_unhide_post_edit_permission_passes_for_thread_post_edit_for_category_moderator(
    user_permissions_factory, user, post
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[post.category_id],
    )

    post_edit = create_post_edit(post=post, user="DeletedUser")

    permissions = user_permissions_factory(user)
    check_unhide_post_edit_permission(permissions, post_edit)


def test_check_unhide_post_edit_permission_passes_for_private_thread_post_edit_for_global_moderator(
    user_permissions_factory, moderator, private_thread
):
    post = private_thread.first_post
    post_edit = create_post_edit(post=post, user="DeletedUser")

    permissions = user_permissions_factory(moderator)
    check_unhide_post_edit_permission(permissions, post_edit)


def test_check_unhide_post_edit_permission_passes_for_private_thread_post_edit_for_private_threads_moderator(
    user_permissions_factory, user, private_thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    post = private_thread.first_post
    post_edit = create_post_edit(post=post, user="DeletedUser")

    permissions = user_permissions_factory(user)
    check_unhide_post_edit_permission(permissions, post_edit)


def test_check_unhide_post_edit_permission_fails_user_without_moderator_permissions(
    user_permissions_factory, user, post
):
    post_edit = create_post_edit(post=post, user="DeletedUser")

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_unhide_post_edit_permission(permissions, post_edit)


def test_check_delete_post_edit_permission_passes_for_thread_post_edit_for_global_moderator(
    user_permissions_factory, moderator, post
):
    post_edit = create_post_edit(post=post, user="DeletedUser")

    permissions = user_permissions_factory(moderator)
    check_delete_post_edit_permission(permissions, post_edit)


def test_check_delete_post_edit_permission_passes_for_thread_post_edit_for_category_moderator(
    user_permissions_factory, user, post
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[post.category_id],
    )

    post_edit = create_post_edit(post=post, user="DeletedUser")

    permissions = user_permissions_factory(user)
    check_delete_post_edit_permission(permissions, post_edit)


def test_check_delete_post_edit_permission_passes_for_private_thread_post_edit_for_global_moderator(
    user_permissions_factory, moderator, private_thread
):
    post = private_thread.first_post
    post_edit = create_post_edit(post=post, user="DeletedUser")

    permissions = user_permissions_factory(moderator)
    check_delete_post_edit_permission(permissions, post_edit)


def test_check_delete_post_edit_permission_passes_for_private_thread_post_edit_for_private_threads_moderator(
    user_permissions_factory, user, private_thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    post = private_thread.first_post
    post_edit = create_post_edit(post=post, user="DeletedUser")

    permissions = user_permissions_factory(user)
    check_delete_post_edit_permission(permissions, post_edit)


def test_check_delete_post_edit_permission_fails_user_for_deleted_user_post_edit(
    user_permissions_factory, user, post
):
    post_edit = create_post_edit(post=post, user="DeletedUser")

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_delete_post_edit_permission(permissions, post_edit)


def test_check_delete_post_edit_permission_fails_user_for_other_user_post_edit(
    user_permissions_factory, user, other_user, post
):
    post_edit = create_post_edit(post=post, user=other_user)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_delete_post_edit_permission(permissions, post_edit)


def test_check_delete_post_edit_permission_fails_user_with_hide_permission_for_own_post_edit(
    user_permissions_factory, user, members_group, post
):
    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.HIDE
    members_group.save()

    post_edit = create_post_edit(post=post, user=user)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_delete_post_edit_permission(permissions, post_edit)


def test_check_delete_post_edit_permission_fails_user_without_hide_permission_for_own_post_edit(
    user_permissions_factory, user, members_group, post
):
    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.NEVER
    members_group.save()

    post_edit = create_post_edit(post=post, user=user)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_delete_post_edit_permission(permissions, post_edit)


def test_check_delete_post_edit_permission_passes_user_with_delete_permission_for_own_post_edit(
    user_permissions_factory, user, members_group, post
):
    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    post_edit = create_post_edit(post=post, user=user)

    permissions = user_permissions_factory(user)
    check_delete_post_edit_permission(permissions, post_edit)


def test_check_delete_post_edit_permission_passes_user_with_delete_permission_for_own_post_edit_if_its_within_time_limit(
    user_permissions_factory, user, members_group, post
):
    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.own_post_edits_hide_time_limit = 90
    members_group.save()

    post_edit = create_post_edit(post=post, user=user)
    post_edit.edited_at -= timedelta(minutes=30)

    permissions = user_permissions_factory(user)
    check_delete_post_edit_permission(permissions, post_edit)


def test_check_delete_post_edit_permission_fails_user_with_delete_permission_for_own_post_edit_if_its_too_old(
    user_permissions_factory, user, members_group, post
):
    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.own_post_edits_hide_time_limit = 30
    members_group.save()

    post_edit = create_post_edit(post=post, user=user)
    post_edit.edited_at -= timedelta(hours=6)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_delete_post_edit_permission(permissions, post_edit)


def test_check_delete_post_edit_permission_fails_user_with_delete_permission_for_own_post_edit_if_it_hidden_by_other_user(
    user_permissions_factory, user, moderator, members_group, post
):
    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    post_edit = create_post_edit(post=post, user=user)
    hide_post_edit(post_edit, moderator)

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_delete_post_edit_permission(permissions, post_edit)


def test_check_delete_post_edit_permission_fails_user_with_delete_permission_for_own_post_edit_if_it_hidden_by_deleted_user(
    user_permissions_factory, user, members_group, post
):
    members_group.can_hide_own_post_edits = CanHideOwnPostEdits.DELETE
    members_group.save()

    post_edit = create_post_edit(post=post, user=user)
    hide_post_edit(post_edit, "Moderator")

    permissions = user_permissions_factory(user)

    with pytest.raises(PermissionDenied):
        check_delete_post_edit_permission(permissions, post_edit)
