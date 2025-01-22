import pytest
from django.core.exceptions import PermissionDenied
from django.http import Http404

from ..posts import check_see_post_permission
from ..enums import CategoryPermission
from ..models import CategoryGroupPermission, Moderator
from ..proxy import UserPermissionsProxy


def test_check_see_post_permission_passes_user_with_permission_to_see_thread_post(
    user, cache_versions, post
):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_fails_user_without_category_permission(
    user, cache_versions, post
):
    CategoryGroupPermission.objects.filter(
        category=post.category, permission=CategoryPermission.BROWSE
    ).delete()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_fails_user_without_thread_permission(
    user, cache_versions, post
):
    post.thread.is_hidden = True
    post.thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_fails_global_moderator_without_category_permission(
    moderator, cache_versions, post
):
    CategoryGroupPermission.objects.filter(
        category=post.category, permission=CategoryPermission.BROWSE
    ).delete()

    permissions = UserPermissionsProxy(moderator, cache_versions)

    with pytest.raises(Http404):
        check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_passes_unapproved_post_poster(
    user, cache_versions, post
):
    post.poster = user
    post.is_unapproved = True
    post.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_passes_moderator_with_unapproved_post_access(
    moderator, cache_versions, post
):
    post.is_unapproved = True
    post.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_fails_user_without_unapproved_post_access(
    user, cache_versions, post
):
    post.is_unapproved = True
    post.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_passes_global_moderator_with_hidden_post_access(
    moderator, cache_versions, post
):
    post.is_hidden = True
    post.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_fails_user_without_hidden_post_access(
    user, cache_versions, post
):
    post.is_hidden = True
    post.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_passes_user_with_permission_to_see_private_thread_post(
    user, cache_versions, private_threads_category, user_private_thread
):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_post_permission(
        permissions,
        private_threads_category,
        user_private_thread,
        user_private_thread.first_post,
    )


def test_check_see_post_permission_fails_user_without_private_threads_permission(
    user, members_group, cache_versions, private_threads_category, user_private_thread
):
    members_group.can_use_private_threads = False
    members_group.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_see_post_permission(
            permissions,
            private_threads_category,
            user_private_thread,
            user_private_thread.first_post,
        )


def test_check_see_post_permission_fails_user_without_private_thread_access(
    user, cache_versions, private_threads_category, private_thread
):
    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_see_post_permission(
            permissions,
            private_threads_category,
            private_thread,
            private_thread.first_post,
        )
