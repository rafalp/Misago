import pytest
from django.core.exceptions import PermissionDenied
from django.http import Http404

from ..enums import CategoryPermission
from ..models import CategoryGroupPermission, Moderator
from ..proxy import UserPermissionsProxy
from ..threads import (
    check_post_in_closed_category_permission,
    check_see_thread_permission,
    check_start_thread_in_category_permission,
)


def test_check_post_in_closed_category_permission_passes_if_category_is_open(
    user, cache_versions, default_category
):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_post_in_closed_category_permission(permissions, default_category)


def test_check_post_in_closed_category_permission_passes_if_user_is_global_moderator(
    moderator, cache_versions, default_category
):
    default_category.is_closed = True
    default_category.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_post_in_closed_category_permission(permissions, default_category)


def test_check_post_in_closed_category_permission_passes_if_user_is_category_moderator(
    user, cache_versions, default_category
):
    default_category.is_closed = True
    default_category.save()

    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    permissions = UserPermissionsProxy(user, cache_versions)
    check_post_in_closed_category_permission(permissions, default_category)


def test_check_post_in_closed_category_permission_fails_if_user_is_not_moderator(
    user, cache_versions, default_category
):
    default_category.is_closed = True
    default_category.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_post_in_closed_category_permission(permissions, default_category)


def test_check_post_in_closed_category_permission_fails_if_user_is_anonymous(
    anonymous_user, cache_versions, default_category
):
    default_category.is_closed = True
    default_category.save()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_post_in_closed_category_permission(permissions, default_category)


def test_check_start_thread_in_category_permission_passes_if_user_has_permission(
    user, cache_versions, default_category
):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_start_thread_in_category_permission(permissions, default_category)


def test_check_start_thread_in_category_permission_passes_if_anonymous_has_permission(
    user, cache_versions, default_category
):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_start_thread_in_category_permission(permissions, default_category)


def test_check_start_thread_in_category_permission_fails_if_user_has_no_permission(
    user, cache_versions, default_category
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.START,
    ).delete()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_start_thread_in_category_permission(permissions, default_category)


def test_check_start_thread_in_category_permission_fails_if_anonymous_has_no_permission(
    anonymous_user, guests_group, cache_versions, default_category
):
    CategoryGroupPermission.objects.filter(
        group=guests_group,
        permission=CategoryPermission.START,
    ).delete()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_start_thread_in_category_permission(permissions, default_category)


def test_check_start_thread_in_category_permission_passes_if_user_is_global_moderator(
    moderator, cache_versions, default_category
):
    default_category.is_closed = True
    default_category.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_start_thread_in_category_permission(permissions, default_category)


def test_check_start_thread_in_category_permission_passes_if_user_is_category_moderator(
    user, cache_versions, default_category
):
    default_category.is_closed = True
    default_category.save()

    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    permissions = UserPermissionsProxy(user, cache_versions)
    check_start_thread_in_category_permission(permissions, default_category)


def test_check_start_thread_in_category_permission_fails_for_user_if_category_is_closed(
    user, cache_versions, default_category
):
    default_category.is_closed = True
    default_category.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_start_thread_in_category_permission(permissions, default_category)


def test_check_start_thread_in_category_permission_fails_for_anonymous_if_category_is_closed(
    anonymous_user, cache_versions, default_category
):
    default_category.is_closed = True
    default_category.save()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_start_thread_in_category_permission(permissions, default_category)


def test_check_see_thread_permission_passes_for_user_with_permission(
    user, cache_versions, default_category, thread
):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_thread_permission(permissions, default_category, thread)


def test_check_see_thread_permission_passes_for_anonymous_user_with_permission(
    anonymous_user, cache_versions, default_category, thread
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    check_see_thread_permission(permissions, default_category, thread)


def test_check_see_thread_permission_passes_for_user_viewing_their_unapproved_thread(
    user, cache_versions, default_category, thread
):
    thread.starter = user
    thread.is_unapproved = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_thread_permission(permissions, default_category, thread)


def test_check_see_thread_permission_fails_for_user_viewing_other_user_unapproved_thread(
    user, other_user, cache_versions, default_category, thread
):
    thread.starter = other_user
    thread.is_unapproved = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_see_thread_permission(permissions, default_category, thread)


def test_check_see_thread_permission_fails_for_user_viewing_deleted_user_unapproved_thread(
    user, cache_versions, default_category, thread
):
    thread.is_unapproved = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_see_thread_permission(permissions, default_category, thread)


def test_check_see_thread_permission_passes_for_category_moderator_viewing_their_unapproved_thread(
    user, cache_versions, default_category, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    thread.starter = user
    thread.is_unapproved = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_thread_permission(permissions, default_category, thread)


def test_check_see_thread_permission_passes_for_category_moderator_viewing_other_user_unapproved_thread(
    user, other_user, cache_versions, default_category, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    thread.starter = other_user
    thread.is_unapproved = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_thread_permission(permissions, default_category, thread)


def test_check_see_thread_permission_passes_for_category_moderator_viewing_deleted_user_unapproved_thread(
    user, cache_versions, default_category, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    thread.is_unapproved = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_thread_permission(permissions, default_category, thread)


def test_check_see_thread_permission_passes_for_global_moderator_viewing_their_unapproved_thread(
    moderator, cache_versions, default_category, thread
):
    thread.starter = moderator
    thread.is_unapproved = True
    thread.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_see_thread_permission(permissions, default_category, thread)


def test_check_see_thread_permission_passes_for_global_moderator_viewing_other_user_unapproved_thread(
    moderator, other_user, cache_versions, default_category, thread
):

    thread.starter = other_user
    thread.is_unapproved = True
    thread.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_see_thread_permission(permissions, default_category, thread)


def test_check_see_thread_permission_passes_for_global_moderator_viewing_deleted_user_unapproved_thread(
    moderator, cache_versions, default_category, thread
):
    thread.is_unapproved = True
    thread.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_see_thread_permission(permissions, default_category, thread)


def test_check_see_thread_permission_fails_for_anonymous_user_viewing_user_unapproved_thread(
    anonymous_user, user, cache_versions, default_category, thread
):

    thread.starter = user
    thread.is_unapproved = True
    thread.save()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    with pytest.raises(Http404):
        check_see_thread_permission(permissions, default_category, thread)


def test_check_see_thread_permission_fails_for_anonymous_user_viewing_deleted_user_unapproved_thread(
    anonymous_user, cache_versions, default_category, thread
):
    thread.is_unapproved = True
    thread.save()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    with pytest.raises(Http404):
        check_see_thread_permission(permissions, default_category, thread)


def test_check_see_thread_permission_fails_for_user_viewing_their_hidden_thread(
    user, cache_versions, default_category, thread
):
    thread.starter = user
    thread.is_hidden = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_see_thread_permission(permissions, default_category, thread)


def test_check_see_thread_permission_fails_for_user_viewing_other_user_hidden_thread(
    user, other_user, cache_versions, default_category, thread
):
    thread.starter = other_user
    thread.is_hidden = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_see_thread_permission(permissions, default_category, thread)


def test_check_see_thread_permission_fails_for_user_viewing_deleted_user_hidden_thread(
    user, cache_versions, default_category, thread
):
    thread.is_hidden = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_see_thread_permission(permissions, default_category, thread)


def test_check_see_thread_permission_passes_for_category_moderator_viewing_their_hidden_thread(
    user, cache_versions, default_category, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    thread.starter = user
    thread.is_hidden = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_thread_permission(permissions, default_category, thread)


def test_check_see_thread_permission_passes_for_category_moderator_viewing_other_user_hidden_thread(
    user, other_user, cache_versions, default_category, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    thread.starter = other_user
    thread.is_hidden = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_thread_permission(permissions, default_category, thread)


def test_check_see_thread_permission_passes_for_category_moderator_viewing_deleted_user_hidden_thread(
    user, cache_versions, default_category, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    thread.is_hidden = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_thread_permission(permissions, default_category, thread)


def test_check_see_thread_permission_passes_for_global_moderator_viewing_their_hidden_thread(
    moderator, cache_versions, default_category, thread
):
    thread.starter = moderator
    thread.is_hidden = True
    thread.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_see_thread_permission(permissions, default_category, thread)


def test_check_see_thread_permission_passes_for_global_moderator_viewing_other_user_hidden_thread(
    moderator, other_user, cache_versions, default_category, thread
):
    thread.starter = other_user
    thread.is_hidden = True
    thread.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_see_thread_permission(permissions, default_category, thread)


def test_check_see_thread_permission_passes_for_global_moderator_viewing_deleted_user_hidden_thread(
    moderator, cache_versions, default_category, thread
):
    thread.is_hidden = True
    thread.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_see_thread_permission(permissions, default_category, thread)


def test_check_see_thread_permission_fails_for_anonymous_user_viewing_user_hidden_thread(
    anonymous_user, other_user, cache_versions, default_category, thread
):
    thread.starter = other_user
    thread.is_hidden = True
    thread.save()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    with pytest.raises(Http404):
        check_see_thread_permission(permissions, default_category, thread)


def test_check_see_thread_permission_fails_for_anonymous_user_viewing_deleted_user_hidden_thread(
    anonymous_user, cache_versions, default_category, thread
):
    thread.is_hidden = True
    thread.save()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    with pytest.raises(Http404):
        check_see_thread_permission(permissions, default_category, thread)


def test_check_see_thread_permission_fails_for_user_without_see_permission(
    user, cache_versions, default_category, thread
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.SEE,
    ).delete()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_see_thread_permission(permissions, default_category, thread)


def test_check_see_thread_permission_fails_for_anonymous_user_without_see_permission(
    anonymous_user, guests_group, cache_versions, default_category, thread
):
    CategoryGroupPermission.objects.filter(
        group=guests_group,
        permission=CategoryPermission.SEE,
    ).delete()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    with pytest.raises(Http404):
        check_see_thread_permission(permissions, default_category, thread)


def test_check_see_thread_permission_fails_for_user_without_browse_permission(
    user, cache_versions, default_category, thread
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.BROWSE,
    ).delete()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_see_thread_permission(permissions, default_category, thread)


def test_check_see_thread_permission_fails_for_anonymous_user_without_browse_permission(
    anonymous_user, guests_group, cache_versions, default_category, thread
):
    CategoryGroupPermission.objects.filter(
        group=guests_group,
        permission=CategoryPermission.BROWSE,
    ).delete()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    with pytest.raises(Http404):
        check_see_thread_permission(permissions, default_category, thread)


def test_check_see_thread_permission_fails_for_user_without_browse_permission_in_delayed_check_category(
    user, cache_versions, default_category, thread
):
    default_category.delay_browse_check = True
    default_category.save()

    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.BROWSE,
    ).delete()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_see_thread_permission(permissions, default_category, thread)


def test_check_see_thread_permission_fails_for_anonymous_user_without_browse_permission_in_delayed_check_category(
    anonymous_user, guests_group, cache_versions, default_category, thread
):
    default_category.delay_browse_check = True
    default_category.save()

    CategoryGroupPermission.objects.filter(
        group=guests_group,
        permission=CategoryPermission.BROWSE,
    ).delete()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_see_thread_permission(permissions, default_category, thread)
