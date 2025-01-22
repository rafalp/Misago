import pytest
from django.core.exceptions import PermissionDenied
from django.http import Http404

from ..enums import CategoryPermission
from ..models import CategoryGroupPermission, Moderator
from ..proxy import UserPermissionsProxy
from ..threads import (
    check_edit_thread_post_permission,
    check_edit_thread_permission,
    check_post_in_closed_category_permission,
    check_post_in_closed_thread_permission,
    check_reply_thread_permission,
    check_see_thread_post_permission,
    check_see_thread_permission,
    check_start_thread_permission,
)


def test_check_edit_thread_post_permission_passes_if_user_is_poster(
    user, thread, user_reply, cache_versions, default_category
):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_edit_thread_post_permission(permissions, default_category, thread, user_reply)


def test_check_edit_thread_post_permission_passes_if_user_is_poster_in_time_limit(
    user, thread, user_reply, cache_versions, default_category
):
    user.group.own_posts_edit_time_limit = 5
    user.group.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_edit_thread_post_permission(permissions, default_category, thread, user_reply)


def test_check_edit_thread_post_permission_fails_if_user_has_no_reply_permission(
    user, thread, user_reply, cache_versions, default_category
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        category=default_category,
        permission=CategoryPermission.REPLY,
    ).delete()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_edit_thread_post_permission(
            permissions, default_category, thread, user_reply
        )


def test_check_edit_thread_post_permission_fails_if_user_has_no_edit_permission(
    user, thread, user_reply, cache_versions, default_category
):
    user.group.can_edit_own_posts = False
    user.group.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_edit_thread_post_permission(
            permissions, default_category, thread, user_reply
        )


def test_check_edit_thread_post_permission_fails_if_user_is_not_poster(
    user, thread, reply, cache_versions, default_category
):
    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_edit_thread_post_permission(permissions, default_category, thread, reply)


def test_check_edit_thread_post_permission_fails_if_user_is_poster_out_of_time_limit(
    user, thread, user_reply, cache_versions, default_category
):
    user.group.own_posts_edit_time_limit = 1
    user.group.save()

    user_reply.posted_on = user_reply.posted_on.replace(year=2015)
    user_reply.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_edit_thread_post_permission(
            permissions, default_category, thread, user_reply
        )


def test_check_edit_thread_post_permission_fails_if_category_is_closed(
    user, thread, user_reply, cache_versions, default_category
):
    default_category.is_closed = True
    default_category.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_edit_thread_post_permission(
            permissions, default_category, thread, user_reply
        )


def test_check_edit_thread_post_permission_fails_if_thread_is_closed(
    user, thread, user_reply, cache_versions, default_category
):
    thread.is_closed = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_edit_thread_post_permission(
            permissions, default_category, thread, user_reply
        )


def test_check_edit_thread_post_permission_fails_if_post_is_protected(
    user, thread, user_reply, cache_versions, default_category
):
    user_reply.is_protected = True
    user_reply.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_edit_thread_post_permission(
            permissions, default_category, thread, user_reply
        )


def test_check_edit_thread_post_permission_fails_if_post_is_hidden(
    user, thread, user_reply, cache_versions, default_category
):
    user_reply.is_hidden = True
    user_reply.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_edit_thread_post_permission(
            permissions, default_category, thread, user_reply
        )


def test_check_edit_thread_post_permission_passes_for_global_moderator_if_category_is_closed(
    moderator, thread, user_reply, cache_versions, default_category
):
    default_category.is_closed = True
    default_category.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_edit_thread_post_permission(permissions, default_category, thread, user_reply)


def test_check_edit_thread_post_permission_passes_for_category_moderator_if_category_is_closed(
    user, thread, reply, cache_versions, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    default_category.is_closed = True
    default_category.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_edit_thread_post_permission(permissions, default_category, thread, reply)


def test_check_edit_thread_post_permission_passes_for_global_moderator_if_thread_is_closed(
    moderator, thread, user_reply, cache_versions, default_category
):
    thread.is_closed = True
    thread.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_edit_thread_post_permission(permissions, default_category, thread, user_reply)


def test_check_edit_thread_post_permission_passes_for_category_moderator_if_thread_is_closed(
    user, thread, reply, cache_versions, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    thread.is_closed = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_edit_thread_post_permission(permissions, default_category, thread, reply)


def test_check_edit_thread_post_permission_passes_for_global_moderator_if_post_is_protected(
    moderator, thread, user_reply, cache_versions, default_category
):
    user_reply.is_protected = True
    user_reply.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_edit_thread_post_permission(permissions, default_category, thread, user_reply)


def test_check_edit_thread_post_permission_passes_for_category_moderator_if_post_is_protected(
    user, thread, reply, cache_versions, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    reply.is_protected = True
    reply.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_edit_thread_post_permission(permissions, default_category, thread, reply)


def test_check_edit_thread_post_permission_passes_for_global_moderator_if_post_is_hidden(
    moderator, thread, user_reply, cache_versions, default_category
):
    user_reply.is_hidden = True
    user_reply.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_edit_thread_post_permission(permissions, default_category, thread, user_reply)


def test_check_edit_thread_post_permission_passes_for_category_moderator_if_post_is_hidden(
    user, thread, reply, cache_versions, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    reply.is_hidden = True
    reply.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_edit_thread_post_permission(permissions, default_category, thread, reply)


def test_check_edit_thread_post_permission_passes_for_global_moderator_if_out_of_time(
    moderator, thread, user_reply, cache_versions, default_category
):
    moderator.group.own_posts_edit_time_limit = 1
    moderator.group.save()

    user_reply.posted_on = user_reply.posted_on.replace(year=2015)
    user_reply.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_edit_thread_post_permission(permissions, default_category, thread, user_reply)


def test_check_edit_thread_post_permission_passes_for_category_moderator_if_out_of_time(
    user, thread, reply, cache_versions, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    user.group.own_posts_edit_time_limit = 1
    user.group.save()

    reply.posted_on = reply.posted_on.replace(year=2015)
    reply.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_edit_thread_post_permission(permissions, default_category, thread, reply)


def test_check_edit_thread_permission_passes_if_user_is_starter(
    user, user_thread, cache_versions, default_category
):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_edit_thread_permission(permissions, default_category, user_thread)


def test_check_edit_thread_permission_passes_if_user_is_starter_in_time_limit(
    user, user_thread, cache_versions, default_category
):
    user.group.own_threads_edit_time_limit = 5
    user.group.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_edit_thread_permission(permissions, default_category, user_thread)


def test_check_edit_thread_permission_fails_if_user_has_no_start_permission(
    user, user_thread, cache_versions, default_category
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        category=default_category,
        permission=CategoryPermission.START,
    ).delete()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_edit_thread_permission(permissions, default_category, user_thread)


def test_check_edit_thread_permission_fails_if_user_has_no_edit_permission(
    user, user_thread, cache_versions, default_category
):
    user.group.can_edit_own_threads = False
    user.group.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_edit_thread_permission(permissions, default_category, user_thread)


def test_check_edit_thread_permission_fails_if_user_is_not_starter(
    user, thread, cache_versions, default_category
):
    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_edit_thread_permission(permissions, default_category, thread)


def test_check_edit_thread_permission_fails_if_user_is_starter_out_of_time_limit(
    user, user_thread, cache_versions, default_category
):
    user.group.own_threads_edit_time_limit = 1
    user.group.save()

    user_thread.started_on = user_thread.started_on.replace(year=2015)
    user_thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_edit_thread_permission(permissions, default_category, user_thread)


def test_check_edit_thread_permission_fails_if_category_is_closed(
    user, user_thread, cache_versions, default_category
):
    default_category.is_closed = True
    default_category.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_edit_thread_permission(permissions, default_category, user_thread)


def test_check_edit_thread_permission_fails_if_thread_is_closed(
    user, user_thread, cache_versions, default_category
):
    user_thread.is_closed = True
    user_thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_edit_thread_permission(permissions, default_category, user_thread)


def test_check_edit_thread_permission_passes_for_global_moderator_if_category_is_closed(
    moderator, user_thread, cache_versions, default_category
):
    default_category.is_closed = True
    default_category.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_edit_thread_permission(permissions, default_category, user_thread)


def test_check_edit_thread_permission_passes_for_category_moderator_if_category_is_closed(
    user, thread, cache_versions, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    default_category.is_closed = True
    default_category.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_edit_thread_permission(permissions, default_category, thread)


def test_check_edit_thread_permission_passes_for_global_moderator_if_thread_is_closed(
    moderator, user_thread, cache_versions, default_category
):
    user_thread.is_closed = True
    user_thread.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_edit_thread_permission(permissions, default_category, user_thread)


def test_check_edit_thread_permission_passes_for_category_moderator_if_thread_is_closed(
    user, thread, cache_versions, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    thread.is_closed = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_edit_thread_permission(permissions, default_category, thread)


def test_check_edit_thread_permission_passes_for_global_moderator_if_out_of_time(
    moderator, thread, cache_versions, default_category
):
    moderator.group.own_threads_edit_time_limit = 1
    moderator.group.save()

    thread.started_on = thread.started_on.replace(year=2015)
    thread.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_edit_thread_permission(permissions, default_category, thread)


def test_check_edit_thread_permission_passes_for_category_moderator_if_out_of_time(
    user, thread, cache_versions, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    user.group.own_threads_edit_time_limit = 1
    user.group.save()

    thread.started_on = thread.started_on.replace(year=2015)
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_edit_thread_permission(permissions, default_category, thread)


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


def test_check_post_in_closed_thread_permission_passes_if_thread_is_open(
    user, cache_versions, thread
):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_post_in_closed_thread_permission(permissions, thread)


def test_check_post_in_closed_thread_permission_passes_if_user_is_global_moderator(
    moderator, cache_versions, thread
):
    thread.is_closed = True
    thread.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_post_in_closed_thread_permission(permissions, thread)


def test_check_post_in_closed_thread_permission_passes_if_user_is_category_moderator(
    user, cache_versions, thread
):
    thread.is_closed = True
    thread.save()

    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    permissions = UserPermissionsProxy(user, cache_versions)
    check_post_in_closed_thread_permission(permissions, thread)


def test_check_post_in_closed_thread_permission_fails_if_user_is_not_moderator(
    user, cache_versions, thread
):
    thread.is_closed = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_post_in_closed_thread_permission(permissions, thread)


def test_check_post_in_closed_thread_permission_fails_if_user_is_anonymous(
    anonymous_user, cache_versions, thread
):
    thread.is_closed = True
    thread.save()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_post_in_closed_thread_permission(permissions, thread)


def test_check_reply_thread_permission_passes_if_user_has_permission(
    user, cache_versions, default_category, thread
):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_reply_thread_permission(permissions, default_category, thread)


def test_check_reply_thread_permission_passes_if_anonymous_user_has_permission(
    anonymous_user, cache_versions, default_category, thread
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    check_reply_thread_permission(permissions, default_category, thread)


def test_check_reply_thread_permission_fails_if_user_has_no_permission(
    user, cache_versions, default_category, thread
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.REPLY,
    ).delete()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_reply_thread_permission(permissions, default_category, thread)


def test_check_reply_thread_permission_fails_if_anonymous_has_no_permission(
    anonymous_user, guests_group, cache_versions, default_category, thread
):
    CategoryGroupPermission.objects.filter(
        group=guests_group,
        permission=CategoryPermission.REPLY,
    ).delete()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_reply_thread_permission(permissions, default_category, thread)


def test_check_reply_thread_permission_in_closed_category_passes_if_user_is_global_moderator(
    moderator, cache_versions, default_category, thread
):
    default_category.is_closed = True
    default_category.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_reply_thread_permission(permissions, default_category, thread)


def test_check_reply_thread_permission_in_closed_category_passes_if_user_is_category_moderator(
    user, cache_versions, default_category, thread
):
    default_category.is_closed = True
    default_category.save()

    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    permissions = UserPermissionsProxy(user, cache_versions)
    check_reply_thread_permission(permissions, default_category, thread)


def test_check_reply_thread_permission_fails_for_user_if_category_is_closed(
    user, cache_versions, default_category, thread
):
    default_category.is_closed = True
    default_category.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_reply_thread_permission(permissions, default_category, thread)


def test_check_reply_thread_permission_fails_for_anonymous_if_category_is_closed(
    anonymous_user, cache_versions, default_category, thread
):
    default_category.is_closed = True
    default_category.save()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_reply_thread_permission(permissions, default_category, thread)


def test_check_reply_thread_permission_in_closed_thread_passes_if_user_is_global_moderator(
    moderator, cache_versions, default_category, thread
):
    thread.is_closed = True
    thread.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_reply_thread_permission(permissions, default_category, thread)


def test_check_reply_thread_permission_in_closed_thread_passes_if_user_is_category_moderator(
    user, cache_versions, default_category, thread
):
    thread.is_closed = True
    thread.save()

    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    permissions = UserPermissionsProxy(user, cache_versions)
    check_reply_thread_permission(permissions, default_category, thread)


def test_check_reply_thread_permission_fails_for_user_if_thread_is_closed(
    user, cache_versions, default_category, thread
):
    thread.is_closed = True
    thread.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_reply_thread_permission(permissions, default_category, thread)


def test_check_reply_thread_permission_fails_for_anonymous_if_thread_is_closed(
    anonymous_user, cache_versions, default_category, thread
):
    thread.is_closed = True
    thread.save()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_reply_thread_permission(permissions, default_category, thread)


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


def test_check_see_thread_post_permission_passes_if_user_has_permission(
    user, cache_versions, default_category, thread, post
):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_thread_post_permission(permissions, default_category, thread, post)


def test_check_see_thread_post_permission_passes_if_anonymous_has_permission(
    anonymous_user, cache_versions, default_category, thread, post
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    check_see_thread_post_permission(permissions, default_category, thread, post)


def test_check_see_thread_post_permission_passes_if_category_moderator_has_permission(
    user, cache_versions, default_category, thread, post
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_thread_post_permission(permissions, default_category, thread, post)


def test_check_see_thread_post_permission_passes_if_global_moderator_has_permission(
    moderator, cache_versions, default_category, thread, post
):
    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_see_thread_post_permission(permissions, default_category, thread, post)


def test_check_see_thread_post_permission_for_unapproved_post_passes_if_user_is_poster(
    user, cache_versions, default_category, thread, user_reply
):
    user_reply.is_unapproved = True
    user_reply.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_thread_post_permission(permissions, default_category, thread, user_reply)


def test_check_see_thread_post_permission_for_unapproved_post_fails_if_user_is_not_poster(
    user, cache_versions, default_category, thread, other_user_reply
):
    other_user_reply.is_unapproved = True
    other_user_reply.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_see_thread_post_permission(
            permissions, default_category, thread, other_user_reply
        )


def test_check_see_thread_post_permission_for_unapproved_post_fails_if_user_is_anonymous(
    anonymous_user, cache_versions, default_category, thread, user_reply
):
    user_reply.is_unapproved = True
    user_reply.save()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    with pytest.raises(Http404):
        check_see_thread_post_permission(
            permissions, default_category, thread, user_reply
        )


def test_check_see_thread_post_permission_for_unapproved_post_passes_for_category_moderator(
    user, cache_versions, default_category, thread, other_user_reply
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    other_user_reply.is_unapproved = True
    other_user_reply.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_thread_post_permission(
        permissions, default_category, thread, other_user_reply
    )


def test_check_see_thread_post_permission_for_unapproved_post_passes_for_global_moderator(
    moderator, cache_versions, default_category, thread, other_user_reply
):
    other_user_reply.is_unapproved = True
    other_user_reply.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_see_thread_post_permission(
        permissions, default_category, thread, other_user_reply
    )


def test_check_see_thread_post_permission_for_unapproved_anonymous_post_fails_if_user_is_not_moderator(
    user, cache_versions, default_category, thread, post
):
    post.is_unapproved = True
    post.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(Http404):
        check_see_thread_post_permission(permissions, default_category, thread, post)


def test_check_see_thread_post_permission_for_unapproved_anonymous_post_fails_if_user_is_anonymous(
    anonymous_user, cache_versions, default_category, thread, post
):
    post.is_unapproved = True
    post.save()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    with pytest.raises(Http404):
        check_see_thread_post_permission(permissions, default_category, thread, post)


def test_check_see_thread_post_permission_for_unapproved_anonymous_post_passes_for_category_moderator(
    user, cache_versions, default_category, thread, post
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    post.is_unapproved = True
    post.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_thread_post_permission(permissions, default_category, thread, post)


def test_check_see_thread_post_permission_for_unapproved_anonymous_post_passes_for_global_moderator(
    moderator, cache_versions, default_category, thread, post
):
    post.is_unapproved = True
    post.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_see_thread_post_permission(permissions, default_category, thread, post)


def test_check_see_thread_post_permission_for_hidden_post_fails_if_user_is_poster(
    user, cache_versions, default_category, thread, user_reply
):
    user_reply.is_hidden = True
    user_reply.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_see_thread_post_permission(
            permissions, default_category, thread, user_reply
        )


def test_check_see_thread_post_permission_for_hidden_post_fails_if_user_is_not_poster(
    user, cache_versions, default_category, thread, other_user_reply
):
    other_user_reply.is_hidden = True
    other_user_reply.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_see_thread_post_permission(
            permissions, default_category, thread, other_user_reply
        )


def test_check_see_thread_post_permission_for_hidden_post_fails_if_user_is_anonymous(
    anonymous_user, cache_versions, default_category, thread, user_reply
):
    user_reply.is_hidden = True
    user_reply.save()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_see_thread_post_permission(
            permissions, default_category, thread, user_reply
        )


def test_check_see_thread_post_permission_for_hidden_post_passes_for_category_moderator(
    user, cache_versions, default_category, thread, user_reply
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    user_reply.is_hidden = True
    user_reply.save()

    permissions = UserPermissionsProxy(user, cache_versions)
    check_see_thread_post_permission(permissions, default_category, thread, user_reply)


def test_check_see_thread_post_permission_for_hidden_post_passes_for_global_moderator(
    moderator, cache_versions, default_category, thread, user_reply
):
    Moderator.objects.create(
        user=moderator,
        is_global=False,
        categories=[default_category.id],
    )

    user_reply.is_hidden = True
    user_reply.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_see_thread_post_permission(permissions, default_category, thread, user_reply)


def test_check_start_thread_permission_passes_if_user_has_permission(
    user, cache_versions, default_category
):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_start_thread_permission(permissions, default_category)


def test_check_start_thread_permission_passes_if_anonymous_has_permission(
    anonymous_user, cache_versions, default_category
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    check_start_thread_permission(permissions, default_category)


def test_check_start_thread_permission_fails_if_user_has_no_permission(
    user, cache_versions, default_category
):
    CategoryGroupPermission.objects.filter(
        group=user.group,
        permission=CategoryPermission.START,
    ).delete()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_start_thread_permission(permissions, default_category)


def test_check_start_thread_permission_fails_if_anonymous_has_no_permission(
    anonymous_user, guests_group, cache_versions, default_category
):
    CategoryGroupPermission.objects.filter(
        group=guests_group,
        permission=CategoryPermission.START,
    ).delete()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_start_thread_permission(permissions, default_category)


def test_check_start_thread_permission_passes_if_user_is_global_moderator(
    moderator, cache_versions, default_category
):
    default_category.is_closed = True
    default_category.save()

    permissions = UserPermissionsProxy(moderator, cache_versions)
    check_start_thread_permission(permissions, default_category)


def test_check_start_thread_permission_passes_if_user_is_category_moderator(
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
    check_start_thread_permission(permissions, default_category)


def test_check_start_thread_permission_fails_for_user_if_category_is_closed(
    user, cache_versions, default_category
):
    default_category.is_closed = True
    default_category.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_start_thread_permission(permissions, default_category)


def test_check_start_thread_permission_fails_for_anonymous_if_category_is_closed(
    anonymous_user, cache_versions, default_category
):
    default_category.is_closed = True
    default_category.save()

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_start_thread_permission(permissions, default_category)
