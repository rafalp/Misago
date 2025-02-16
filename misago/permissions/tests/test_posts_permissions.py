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


def test_check_see_post_permission_fails_category_moderator_without_category_permission(
    user, cache_versions, post
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[post.category_id],
    )

    CategoryGroupPermission.objects.filter(
        category=post.category, permission=CategoryPermission.BROWSE
    ).delete()

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


def test_check_see_post_permission_fails_user_accessing_anonymous_hidden_thread(
    user, cache_versions, post
):
    post.thread.is_hidden = True
    post.thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_fails_user_accessing_other_user_hidden_thread(
    user, other_user, cache_versions, post
):
    post.thread.starter = other_user
    post.thread.is_hidden = True
    post.thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_fails_user_accessing_own_hidden_thread(
    user, cache_versions, post
):
    post.thread.starter = user
    post.thread.is_hidden = True
    post.thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_passes_category_moderator_accessing_anonymous_hidden_thread(
    user, cache_versions, post
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[post.category_id],
    )

    post.thread.is_hidden = True
    post.thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_passes_category_moderator_accessing_other_user_hidden_thread(
    user, other_user, cache_versions, post
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[post.category_id],
    )

    post.thread.starter = other_user
    post.thread.is_hidden = True
    post.thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_passes_category_moderator_accessing_own_hidden_thread(
    user, cache_versions, post
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[post.category_id],
    )

    post.thread.starter = user
    post.thread.is_hidden = True
    post.thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_passes_global_moderator_accessing_anonymous_hidden_thread(
    moderator, cache_versions, post
):
    post.thread.is_hidden = True
    post.thread.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_passes_global_moderator_accessing_other_user_hidden_thread(
    moderator, user, cache_versions, post
):
    post.thread.starter = user
    post.thread.is_hidden = True
    post.thread.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_passes_global_moderator_accessing_own_hidden_thread(
    moderator, cache_versions, post
):
    post.thread.starter = moderator
    post.thread.is_hidden = True
    post.thread.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_fails_user_accessing_anonymous_unapproved_thread(
    user, cache_versions, post
):
    post.thread.is_unapproved = True
    post.thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_fails_user_accessing_other_user_unapproved_thread(
    user, other_user, cache_versions, post
):
    post.thread.starter = other_user
    post.thread.is_unapproved = True
    post.thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_passes_user_accessing_own_unapproved_thread(
    user, cache_versions, post
):
    post.thread.starter = user
    post.thread.is_unapproved = True
    post.thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_passes_category_moderator_accessing_anonymous_unapproved_thread(
    user, cache_versions, post
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[post.category_id],
    )

    post.thread.is_unapproved = True
    post.thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_passes_category_moderator_accessing_other_user_unapproved_thread(
    user, other_user, cache_versions, post
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[post.category_id],
    )

    post.thread.starter = other_user
    post.thread.is_unapproved = True
    post.thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_passes_category_moderator_accessing_own_unapproved_thread(
    user, cache_versions, post
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[post.category_id],
    )

    post.thread.starter = user
    post.thread.is_unapproved = True
    post.thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_passes_global_moderator_accessing_anonymous_unapproved_thread(
    moderator, cache_versions, post
):
    post.thread.is_unapproved = True
    post.thread.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_passes_global_moderator_accessing_other_user_unapproved_thread(
    moderator, user, cache_versions, post
):
    post.thread.starter = user
    post.thread.is_unapproved = True
    post.thread.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_passes_global_moderator_accessing_own_unapproved_thread(
    moderator, cache_versions, post
):
    post.thread.starter = moderator
    post.thread.is_unapproved = True
    post.thread.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_fails_user_accessing_anonymous_hidden_post(
    user, cache_versions, post
):
    post.is_hidden = True
    post.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_fails_user_accessing_other_user_hidden_post(
    user, other_user, cache_versions, post
):
    post.poster = other_user
    post.is_hidden = True
    post.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_fails_user_accessing_their_own_hidden_post(
    user, cache_versions, post
):
    post.poster = user
    post.is_hidden = True
    post.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_passes_category_moderator_accessing_anonymous_hidden_post(
    user, cache_versions, post
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[post.category_id],
    )

    post.is_hidden = True
    post.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_passes_category_moderator_accessing_other_user_hidden_post(
    user, other_user, cache_versions, post
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[post.category_id],
    )

    post.poster = other_user
    post.is_hidden = True
    post.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_passes_category_moderator_accessing_their_hidden_post(
    user, cache_versions, post
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[post.category_id],
    )

    post.poster = user
    post.is_hidden = True
    post.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_passes_global_moderator_accessing_anonymous_hidden_post(
    moderator, cache_versions, post
):
    post.is_hidden = True
    post.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_passes_global_moderator_accessing_other_user_hidden_post(
    moderator, user, cache_versions, post
):
    post.poster = user
    post.is_hidden = True
    post.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_passes_global_moderator_accessing_their_hidden_post(
    moderator, cache_versions, post
):
    post.poster = moderator
    post.is_hidden = True
    post.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_fails_user_accessing_anonymous_unapproved_post(
    user, cache_versions, post
):
    post.is_unapproved = True
    post.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_fails_user_accessing_other_user_unapproved_post(
    user, other_user, cache_versions, post
):
    post.poster = other_user
    post.is_unapproved = True
    post.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_passes_user_accessing_their_unapproved_post(
    user, cache_versions, post
):
    post.poster = user
    post.is_unapproved = True
    post.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_passes_category_moderator_accessing_anonymous_unapproved_post(
    user, cache_versions, post
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[post.category_id],
    )

    post.is_unapproved = True
    post.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_passes_category_moderator_accessing_other_user_unapproved_post(
    user, other_user, cache_versions, post
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[post.category_id],
    )

    post.poster = other_user
    post.is_unapproved = True
    post.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_passes_category_moderator_accessing_their_unapproved_post(
    user, cache_versions, post
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[post.category_id],
    )

    post.poster = user
    post.is_unapproved = True
    post.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_passes_global_moderator_accessing_anonymous_unapproved_post(
    moderator, cache_versions, post
):
    post.is_unapproved = True
    post.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_passes_global_moderator_accessing_other_user_unapproved_post(
    moderator, user, cache_versions, post
):
    post.poster = user
    post.is_unapproved = True
    post.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_see_post_permission(permissions, post.category, post.thread, post)


def test_check_see_post_permission_passes_global_moderator_accessing_their_unapproved_post(
    moderator, cache_versions, post
):
    post.poster = moderator
    post.is_unapproved = True
    post.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
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


def test_check_see_post_permission_fails_user_without_private_thread_membership(
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
