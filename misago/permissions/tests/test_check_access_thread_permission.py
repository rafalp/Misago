import pytest
from django.http import Http404

from ..generic import check_access_thread_permission
from ..enums import CategoryPermission
from ..models import CategoryGroupPermission, Moderator
from ..proxy import UserPermissionsProxy


def test_check_access_thread_permission_passes_user_with_permission_to_see_thread(
    user, cache_versions, thread
):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_access_thread_permission(permissions, thread.category, thread)


def test_check_access_thread_permission_fails_user_without_category_permission(
    user, cache_versions, thread
):
    CategoryGroupPermission.objects.filter(
        category=thread.category, permission=CategoryPermission.BROWSE
    ).delete()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_access_thread_permission(permissions, thread.category, thread)


def test_check_access_thread_permission_fails_category_moderator_without_category_permission(
    user, cache_versions, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    CategoryGroupPermission.objects.filter(
        category=thread.category, permission=CategoryPermission.BROWSE
    ).delete()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_access_thread_permission(permissions, thread.category, thread)


def test_check_access_thread_permission_fails_global_moderator_without_category_permission(
    moderator, cache_versions, thread
):
    CategoryGroupPermission.objects.filter(
        category=thread.category, permission=CategoryPermission.BROWSE
    ).delete()

    permissions = UserPermissionsProxy(moderator, cache_versions)

    with pytest.raises(Http404):
        check_access_thread_permission(permissions, thread.category, thread)


def test_check_access_thread_permission_fails_user_accessing_anonymous_hidden_thread(
    user, cache_versions, thread
):
    thread.is_hidden = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_access_thread_permission(permissions, thread.category, thread)


def test_check_access_thread_permission_fails_user_accessing_other_user_hidden_thread(
    user, other_user, cache_versions, thread
):
    thread.starter = other_user
    thread.is_hidden = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_access_thread_permission(permissions, thread.category, thread)


def test_check_access_thread_permission_fails_user_accessing_own_hidden_thread(
    user, cache_versions, thread
):
    thread.starter = user
    thread.is_hidden = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_access_thread_permission(permissions, thread.category, thread)


def test_check_access_thread_permission_passes_category_moderator_accessing_anonymous_hidden_thread(
    user, cache_versions, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    thread.is_hidden = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_access_thread_permission(permissions, thread.category, thread)


def test_check_access_thread_permission_passes_category_moderator_accessing_other_user_hidden_thread(
    user, other_user, cache_versions, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    thread.starter = other_user
    thread.is_hidden = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_access_thread_permission(permissions, thread.category, thread)


def test_check_access_thread_permission_passes_category_moderator_accessing_own_hidden_thread(
    user, cache_versions, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    thread.starter = user
    thread.is_hidden = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_access_thread_permission(permissions, thread.category, thread)


def test_check_access_thread_permission_passes_global_moderator_accessing_anonymous_hidden_thread(
    moderator, cache_versions, thread
):
    thread.is_hidden = True
    thread.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_access_thread_permission(permissions, thread.category, thread)


def test_check_access_thread_permission_passes_global_moderator_accessing_other_user_hidden_thread(
    moderator, user, cache_versions, thread
):
    thread.starter = user
    thread.is_hidden = True
    thread.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_access_thread_permission(permissions, thread.category, thread)


def test_check_access_thread_permission_passes_global_moderator_accessing_own_hidden_thread(
    moderator, cache_versions, thread
):
    thread.starter = moderator
    thread.is_hidden = True
    thread.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_access_thread_permission(permissions, thread.category, thread)


def test_check_access_thread_permission_fails_user_accessing_anonymous_unapproved_thread(
    user, cache_versions, thread
):
    thread.is_unapproved = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_access_thread_permission(permissions, thread.category, thread)


def test_check_access_thread_permission_fails_user_accessing_other_user_unapproved_thread(
    user, other_user, cache_versions, thread
):
    thread.starter = other_user
    thread.is_unapproved = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_access_thread_permission(permissions, thread.category, thread)


def test_check_access_thread_permission_passes_user_accessing_own_unapproved_thread(
    user, cache_versions, thread
):
    thread.starter = user
    thread.is_unapproved = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_access_thread_permission(permissions, thread.category, thread)


def test_check_access_thread_permission_passes_category_moderator_accessing_anonymous_unapproved_thread(
    user, cache_versions, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    thread.is_unapproved = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_access_thread_permission(permissions, thread.category, thread)


def test_check_access_thread_permission_passes_category_moderator_accessing_other_user_unapproved_thread(
    user, other_user, cache_versions, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    thread.starter = other_user
    thread.is_unapproved = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_access_thread_permission(permissions, thread.category, thread)


def test_check_access_thread_permission_passes_category_moderator_accessing_own_unapproved_thread(
    user, cache_versions, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    thread.starter = user
    thread.is_unapproved = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_access_thread_permission(permissions, thread.category, thread)


def test_check_access_thread_permission_passes_global_moderator_accessing_anonymous_unapproved_thread(
    moderator, cache_versions, thread
):
    thread.is_unapproved = True
    thread.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_access_thread_permission(permissions, thread.category, thread)


def test_check_access_thread_permission_passes_global_moderator_accessing_other_user_unapproved_thread(
    moderator, user, cache_versions, thread
):
    thread.starter = user
    thread.is_unapproved = True
    thread.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_access_thread_permission(permissions, thread.category, thread)


def test_check_access_thread_permission_passes_global_moderator_accessing_own_unapproved_thread(
    moderator, cache_versions, thread
):
    thread.starter = moderator
    thread.is_unapproved = True
    thread.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_access_thread_permission(permissions, thread.category, thread)


def test_check_access_thread_permission_passes_user_with_permission_to_see_private_thread(
    user, cache_versions, private_threads_category, user_private_thread
):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_access_thread_permission(
        permissions,
        private_threads_category,
        user_private_thread,
    )


def test_check_access_thread_permission_fails_user_without_private_threads_permission(
    user, members_group, cache_versions, private_threads_category, user_private_thread
):
    members_group.can_use_private_threads = False
    members_group.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_access_thread_permission(
            permissions,
            private_threads_category,
            user_private_thread,
        )


def test_check_access_thread_permission_fails_user_without_private_thread_membership(
    user, cache_versions, private_threads_category, private_thread
):
    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_access_thread_permission(
            permissions,
            private_threads_category,
            private_thread,
        )
