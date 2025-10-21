import pytest
from django.core.exceptions import PermissionDenied
from django.http import Http404

from ...privatethreads.models import PrivateThreadMember
from ..models import Moderator
from ..privatethreads import (
    check_change_private_thread_owner_permission,
    check_edit_private_thread_post_permission,
    check_edit_private_thread_permission,
    check_locked_private_thread_permission,
    check_private_threads_permission,
    check_remove_private_thread_member_permission,
    check_reply_private_thread_permission,
    check_see_private_thread_permission,
    check_see_private_thread_post_permission,
    check_start_private_threads_permission,
    filter_private_thread_posts_queryset,
    filter_private_threads_queryset,
)
from ..proxy import UserPermissionsProxy


def test_check_edit_private_thread_post_permission_passes_if_user_is_poster(
    user, private_thread, private_thread_user_reply, cache_versions
):
    PrivateThreadMember.objects.create(thread=private_thread, user=user)

    permissions = UserPermissionsProxy(user, cache_versions)
    check_edit_private_thread_post_permission(
        permissions, private_thread, private_thread_user_reply
    )


def test_check_edit_private_thread_post_permission_passes_if_user_is_poster_in_time_limit(
    user, private_thread, private_thread_user_reply, cache_versions
):
    PrivateThreadMember.objects.create(thread=private_thread, user=user)

    user.group.own_posts_edit_time_limit = 5
    user.group.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_edit_private_thread_post_permission(
        permissions, private_thread, private_thread_user_reply
    )


def test_check_edit_private_thread_post_permission_fails_if_user_has_no_edit_permission(
    user, private_thread, private_thread_user_reply, cache_versions
):
    PrivateThreadMember.objects.create(thread=private_thread, user=user)

    user.group.can_edit_own_posts = False
    user.group.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_edit_private_thread_post_permission(
            permissions, private_thread, private_thread_user_reply
        )


def test_check_edit_private_thread_post_permission_fails_if_user_is_not_poster(
    user, private_thread, private_thread_reply, cache_versions
):
    PrivateThreadMember.objects.create(thread=private_thread, user=user)

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_edit_private_thread_post_permission(
            permissions, private_thread, private_thread_reply
        )


def test_check_edit_private_thread_post_permission_fails_if_user_is_poster_out_of_time_limit(
    user, private_thread, private_thread_user_reply, cache_versions
):
    PrivateThreadMember.objects.create(thread=private_thread, user=user)

    user.group.own_posts_edit_time_limit = 1
    user.group.save()

    private_thread_user_reply.posted_at = private_thread_user_reply.posted_at.replace(
        year=2015
    )
    private_thread_user_reply.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_edit_private_thread_post_permission(
            permissions, private_thread, private_thread_user_reply
        )


def test_check_edit_private_thread_post_permission_fails_if_post_is_protected(
    user, private_thread, private_thread_user_reply, cache_versions
):
    PrivateThreadMember.objects.create(thread=private_thread, user=user)

    private_thread_user_reply.is_protected = True
    private_thread_user_reply.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_edit_private_thread_post_permission(
            permissions, private_thread, private_thread_user_reply
        )


def test_check_edit_private_thread_post_permission_fails_if_post_is_hidden(
    user, private_thread, private_thread_user_reply, cache_versions
):
    PrivateThreadMember.objects.create(thread=private_thread, user=user)

    private_thread_user_reply.is_hidden = True
    private_thread_user_reply.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_edit_private_thread_post_permission(
            permissions, private_thread, private_thread_user_reply
        )


def test_check_edit_private_thread_post_permission_passes_for_global_moderator_if_post_is_protected(
    moderator, private_thread, private_thread_user_reply, cache_versions
):
    PrivateThreadMember.objects.create(thread=private_thread, user=moderator)

    private_thread_user_reply.is_protected = True
    private_thread_user_reply.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_edit_private_thread_post_permission(
        permissions, private_thread, private_thread_user_reply
    )


def test_check_edit_private_thread_post_permission_passes_for_private_threads_moderator_if_post_is_protected(
    user, private_thread, private_thread_user_reply, cache_versions
):
    PrivateThreadMember.objects.create(thread=private_thread, user=user)

    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    private_thread_user_reply.is_protected = True
    private_thread_user_reply.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_edit_private_thread_post_permission(
        permissions, private_thread, private_thread_user_reply
    )


def test_check_edit_private_thread_post_permission_passes_for_global_moderator_if_post_is_hidden(
    moderator, private_thread, private_thread_user_reply, cache_versions
):
    PrivateThreadMember.objects.create(thread=private_thread, user=moderator)

    private_thread_user_reply.is_hidden = True
    private_thread_user_reply.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_edit_private_thread_post_permission(
        permissions, private_thread, private_thread_user_reply
    )


def test_check_edit_private_thread_post_permission_passes_for_private_threads_moderator_if_post_is_hidden(
    user, private_thread, private_thread_user_reply, cache_versions
):
    PrivateThreadMember.objects.create(thread=private_thread, user=user)

    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    private_thread_user_reply.is_hidden = True
    private_thread_user_reply.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_edit_private_thread_post_permission(
        permissions, private_thread, private_thread_user_reply
    )


def test_check_edit_private_thread_permission_passes_if_user_is_starter(
    user, user_private_thread, cache_versions
):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_edit_private_thread_permission(permissions, user_private_thread)


def test_check_edit_private_thread_permission_passes_if_user_is_poster_in_time_limit(
    user, user_private_thread, cache_versions
):
    user.group.own_posts_edit_time_limit = 5
    user.group.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_edit_private_thread_permission(permissions, user_private_thread)


def test_check_edit_private_thread_permission_fails_if_user_has_no_edit_permission(
    user, user_private_thread, cache_versions
):
    user.group.can_edit_own_threads = False
    user.group.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_edit_private_thread_permission(permissions, user_private_thread)


def test_check_edit_private_thread_permission_fails_if_user_is_not_thread_owner(
    user, other_user_private_thread, cache_versions
):
    user.group.can_edit_own_threads = False
    user.group.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_edit_private_thread_permission(permissions, other_user_private_thread)


def test_check_edit_private_thread_permission_fails_if_user_is_out_of_time_limit(
    user, user_private_thread, cache_versions
):
    user.group.own_threads_edit_time_limit = 1
    user.group.save()

    user_private_thread.started_at = user_private_thread.started_at.replace(year=2015)
    user_private_thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_edit_private_thread_permission(permissions, user_private_thread)


def test_check_edit_private_thread_permission_passes_for_global_moderator_if_out_of_time(
    moderator, user_private_thread, cache_versions
):
    moderator.group.own_threads_edit_time_limit = 1
    moderator.group.save()

    user_private_thread.started_at = user_private_thread.started_at.replace(year=2015)
    user_private_thread.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_edit_private_thread_permission(permissions, user_private_thread)


def test_check_edit_private_thread_permission_passes_for_private_threads_moderator_if_out_of_time(
    user, user_private_thread, cache_versions
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    user.group.own_threads_edit_time_limit = 1
    user.group.save()

    user_private_thread.started_at = user_private_thread.started_at.replace(year=2015)
    user_private_thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_edit_private_thread_permission(permissions, user_private_thread)


def test_check_locked_private_thread_permission_passes_if_thread_is_open(
    user, cache_versions, thread
):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_locked_private_thread_permission(permissions, thread)


def test_check_locked_private_thread_permission_passes_if_user_is_global_moderator(
    moderator, cache_versions, thread
):
    thread.is_closed = True
    thread.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_locked_private_thread_permission(permissions, thread)


def test_check_locked_private_thread_permission_passes_if_user_is_private_threads_moderator(
    user, cache_versions, thread
):
    thread.is_closed = True
    thread.save()

    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    permissions = UserPermissionsProxy(user, cache_versions)
    check_locked_private_thread_permission(permissions, thread)


def test_check_private_threads_permission_passes_if_user_has_permission(
    user, cache_versions
):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_private_threads_permission(permissions)


def test_check_private_threads_permission_fails_if_user_has_no_permission(
    user, members_group, cache_versions
):
    members_group.can_use_private_threads = False
    members_group.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_private_threads_permission(permissions)


def test_check_private_threads_permission_fails_if_user_is_anonymous(
    anonymous_user, cache_versions
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_private_threads_permission(permissions)


def test_check_start_private_threads_permission_passes_if_user_has_permission(
    user, cache_versions
):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_start_private_threads_permission(permissions)


def test_check_start_private_threads_permission_fails_if_user_has_no_permission(
    user, members_group, cache_versions
):
    members_group.can_start_private_threads = False
    members_group.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_start_private_threads_permission(permissions)


def test_check_reply_private_thread_permission_passes(
    user, cache_versions, user_private_thread
):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_reply_private_thread_permission(permissions, user_private_thread)


def test_check_reply_private_thread_permission_passes_global_moderator(
    moderator, cache_versions, private_thread
):
    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_reply_private_thread_permission(permissions, private_thread)


def test_check_reply_private_thread_permission_fails_user_for_locked_thread(
    user, cache_versions, user_private_thread
):
    user_private_thread.is_closed = True
    user_private_thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_reply_private_thread_permission(permissions, user_private_thread)


def test_check_reply_private_thread_permission_passes_private_threads_moderator_for_locked_thread(
    user, cache_versions, user_private_thread
):
    user_private_thread.is_closed = True
    user_private_thread.save()

    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    permissions = UserPermissionsProxy(user, cache_versions)
    check_reply_private_thread_permission(permissions, user_private_thread)


def test_check_reply_private_thread_permission_passes_global_moderator_for_locked_thread(
    moderator, cache_versions, user_private_thread
):
    user_private_thread.is_closed = True
    user_private_thread.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_reply_private_thread_permission(permissions, user_private_thread)


def test_check_reply_private_thread_permission_fails_for_private_thread_without_other_members(
    user, cache_versions, private_thread
):
    PrivateThreadMember.objects.create(thread=private_thread, user=user)

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_reply_private_thread_permission(permissions, private_thread)


def test_check_reply_private_thread_permission_fails_for_private_thread_without_members(
    user, cache_versions, private_thread
):
    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_reply_private_thread_permission(permissions, private_thread)


def test_check_reply_private_thread_permission_passes_private_threads_moderator_for_private_thread_without_members(
    user, cache_versions, private_thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    permissions = UserPermissionsProxy(user, cache_versions)
    check_reply_private_thread_permission(permissions, private_thread)


def test_check_reply_private_thread_permission_passes_global_moderator_for_private_thread_without_members(
    moderator, cache_versions, private_thread
):
    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_reply_private_thread_permission(permissions, private_thread)


def test_check_see_private_thread_permission_passes_if_user_has_permission(
    user, cache_versions, thread
):
    PrivateThreadMember.objects.create(thread=thread, user=user)

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_private_thread_permission(permissions, thread)


def test_check_see_private_thread_permission_fails_if_user_is_not_thread_member(
    user, cache_versions, thread
):
    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_see_private_thread_permission(permissions, thread)


def test_check_see_private_thread_post_permission_passes_if_user_has_permission(
    user, cache_versions, thread, post
):
    PrivateThreadMember.objects.create(thread=thread, user=user)

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_private_thread_post_permission(permissions, thread, post)


def test_check_see_private_thread_post_permission_for_hidden_post_fails_if_user_is_poster(
    user, cache_versions, thread, user_reply
):
    user_reply.is_hidden = True
    user_reply.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_see_private_thread_post_permission(permissions, thread, user_reply)


def test_check_see_private_thread_post_permission_for_hidden_post_fails_if_user_is_not_poster(
    user, cache_versions, thread, other_user_reply
):
    other_user_reply.is_hidden = True
    other_user_reply.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_see_private_thread_post_permission(permissions, thread, other_user_reply)


def test_check_see_private_thread_post_permission_for_hidden_post_passes_for_private_threads_moderator(
    user, cache_versions, thread, user_reply
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    user_reply.is_hidden = True
    user_reply.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_private_thread_post_permission(permissions, thread, user_reply)


def test_check_see_private_thread_post_permission_for_hidden_post_passes_for_global_moderator(
    moderator, cache_versions, thread, user_reply
):
    user_reply.is_hidden = True
    user_reply.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_see_private_thread_post_permission(permissions, thread, user_reply)


def test_check_change_private_thread_owner_permission_passes_for_thread_owner(
    user, user_private_thread, user_permissions_factory
):
    check_change_private_thread_owner_permission(
        user_permissions_factory(user),
        user_private_thread,
    )


def test_check_change_private_thread_owner_permission_passes_for_moderator(
    moderator, user_private_thread, user_permissions_factory
):
    check_change_private_thread_owner_permission(
        user_permissions_factory(moderator),
        user_private_thread,
    )


def test_check_change_private_thread_owner_permission_fails_for_regular_member(
    other_user, user_private_thread, user_permissions_factory
):
    with pytest.raises(PermissionDenied):
        check_change_private_thread_owner_permission(
            user_permissions_factory(other_user),
            user_private_thread,
        )


def test_check_remove_private_thread_member_permission_passes_for_thread_owner_removing_thread_member(
    user, other_user, user_private_thread, user_permissions_factory
):
    check_remove_private_thread_member_permission(
        user_permissions_factory(user),
        user_private_thread,
        user_permissions_factory(other_user),
    )


def test_check_remove_private_thread_member_permission_passes_for_moderator_removing_thread_member(
    moderator, other_user, user_private_thread, user_permissions_factory
):
    check_remove_private_thread_member_permission(
        user_permissions_factory(moderator),
        user_private_thread,
        user_permissions_factory(other_user),
    )


def test_check_remove_private_thread_member_permission_fails_for_thread_owner_removing_moderator(
    user, moderator, user_private_thread, user_permissions_factory
):
    with pytest.raises(PermissionDenied):
        check_remove_private_thread_member_permission(
            user_permissions_factory(user),
            user_private_thread,
            user_permissions_factory(moderator),
        )


def test_check_remove_private_thread_member_permission_fails_for_thread_member(
    user, other_user, user_private_thread, user_permissions_factory
):
    with pytest.raises(PermissionDenied):
        check_remove_private_thread_member_permission(
            user_permissions_factory(other_user),
            user_private_thread,
            user_permissions_factory(user),
        )


def test_filter_private_threads_queryset_returns_nothing_for_anonymous_user(
    thread_factory, private_threads_category, anonymous_user, cache_versions
):
    thread_factory(private_threads_category)

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    queryset = filter_private_threads_queryset(
        permissions, private_threads_category.thread_set
    )
    assert not queryset.exists()


def test_filter_private_threads_queryset_returns_thread_for_user_who_is_member(
    thread_factory, private_threads_category, user, cache_versions
):
    thread = thread_factory(private_threads_category)
    PrivateThreadMember.objects.create(thread=thread, user=user)

    permissions = UserPermissionsProxy(user, cache_versions)
    queryset = filter_private_threads_queryset(
        permissions, private_threads_category.thread_set
    )
    assert thread in list(queryset)


def test_filter_private_threads_queryset_excludes_thread_user_is_not_member(
    thread_factory, private_threads_category, user, other_user, cache_versions
):
    thread = thread_factory(private_threads_category)
    PrivateThreadMember.objects.create(thread=thread, user=other_user)

    permissions = UserPermissionsProxy(user, cache_versions)
    queryset = filter_private_threads_queryset(
        permissions, private_threads_category.thread_set
    )
    assert not queryset.exists()


def test_filter_private_thread_posts_queryset_returns_all_posts(
    user, cache_versions, thread
):
    permissions = UserPermissionsProxy(user, cache_versions)
    queryset = filter_private_thread_posts_queryset(
        permissions, thread, thread.post_set
    )

    assert queryset.exists()
