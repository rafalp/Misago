from datetime import timedelta

from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.http import Http404
from django.utils import timezone
from django.utils.translation import npgettext, pgettext

from ..threads.models import Post, Thread, ThreadParticipant
from .hooks import (
    check_edit_private_thread_permission_hook,
    check_edit_private_thread_post_permission_hook,
    check_private_threads_permission_hook,
    check_reply_private_thread_permission_hook,
    check_see_private_thread_permission_hook,
    check_see_private_thread_post_permission_hook,
    check_start_private_threads_permission_hook,
    filter_private_thread_posts_queryset_hook,
    filter_private_threads_queryset_hook,
)
from .proxy import UserPermissionsProxy


def check_private_threads_permission(permissions: UserPermissionsProxy):
    check_private_threads_permission_hook(
        _check_private_threads_permission_action, permissions
    )


def _check_private_threads_permission_action(permissions: UserPermissionsProxy):
    if permissions.user.is_anonymous:
        raise PermissionDenied(
            pgettext(
                "private threads permission error",
                "You must be signed in to use private threads.",
            )
        )

    if not permissions.can_use_private_threads:
        raise PermissionDenied(
            pgettext(
                "private threads permission error",
                "You can't use private threads.",
            )
        )


def check_start_private_threads_permission(permissions: UserPermissionsProxy):
    check_start_private_threads_permission_hook(
        _check_start_private_threads_permission_action, permissions
    )


def _check_start_private_threads_permission_action(permissions: UserPermissionsProxy):
    if not permissions.can_start_private_threads:
        raise PermissionDenied(
            pgettext(
                "private threads permission error",
                "You can't start new private threads.",
            )
        )


def check_see_private_thread_permission(
    permissions: UserPermissionsProxy, thread: Thread
):
    check_see_private_thread_permission_hook(
        _check_see_private_thread_permission_action, permissions, thread
    )


def _check_see_private_thread_permission_action(
    permissions: UserPermissionsProxy, thread: Thread
):
    check_private_threads_permission(permissions)

    if permissions.user.id not in thread.private_thread_member_ids:
        raise Http404()


def check_reply_private_thread_permission(
    permissions: UserPermissionsProxy, thread: Thread
):
    check_reply_private_thread_permission_hook(
        _check_see_private_thread_permission_action, permissions, thread
    )


def _check_reply_private_thread_permission_action(
    permissions: UserPermissionsProxy, thread: Thread
):
    pass  # NOOP


def check_edit_private_thread_permission(
    permissions: UserPermissionsProxy, thread: Thread
):
    check_edit_private_thread_permission_hook(
        _check_edit_private_thread_permission_action, permissions, thread
    )


def _check_edit_private_thread_permission_action(
    permissions: UserPermissionsProxy, thread: Thread
):
    if permissions.is_private_threads_moderator:
        return

    if thread.private_thread_member_ids[0] != permissions.user.id:
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "You can't edit other users threads.",
            )
        )

    if not permissions.can_edit_own_threads:
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "You can't edit threads.",
            )
        )

    time_limit = permissions.own_threads_edit_time_limit * 60

    if time_limit and (timezone.now() - thread.started_on).total_seconds() > time_limit:
        raise PermissionDenied(
            npgettext(
                "threads permission error",
                "You can't edit threads older than %(minutes)s minute.",
                "You can't edit threads older than %(minutes)s minutes.",
                permissions.own_threads_edit_time_limit,
            )
        )


def check_see_private_thread_post_permission(
    permissions: UserPermissionsProxy, thread: Thread, post: Post
):
    check_see_private_thread_post_permission_hook(
        _check_see_private_thread_post_permission_action, permissions, thread, post
    )


def _check_see_private_thread_post_permission_action(
    permissions: UserPermissionsProxy, thread: Thread, post: Post
):
    pass


def check_edit_private_thread_post_permission(
    permissions: UserPermissionsProxy, thread: Thread, post: Post
):
    check_edit_private_thread_post_permission_hook(
        _check_edit_private_thread_post_permission_action, permissions, thread, post
    )


def _check_edit_private_thread_post_permission_action(
    permissions: UserPermissionsProxy, thread: Thread, post: Post
):
    if permissions.is_private_threads_moderator:
        return

    user_id = permissions.user.id
    is_poster = user_id and post.poster_id and post.poster_id == user_id

    if not is_poster:
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "You can't edit other users posts.",
            )
        )

    if not permissions.can_edit_own_posts:
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "You can't edit posts.",
            )
        )

    if post.is_hidden:
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "You can't edit hidden posts.",
            )
        )

    if post.is_protected:
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "You can't edit protected posts.",
            )
        )

    time_limit = permissions.own_posts_edit_time_limit * 60

    if time_limit and (timezone.now() - post.posted_on).total_seconds() > time_limit:
        raise PermissionDenied(
            npgettext(
                "threads permission error",
                "You can't edit posts older than %(minutes)s minute.",
                "You can't edit posts older than %(minutes)s minutes.",
                permissions.own_posts_edit_time_limit,
            )
        )


def filter_private_threads_queryset(permissions: UserPermissionsProxy, queryset):
    return filter_private_threads_queryset_hook(
        _filter_private_threads_queryset_action, permissions, queryset
    )


def _filter_private_threads_queryset_action(
    permissions: UserPermissionsProxy, queryset
):
    if permissions.user.is_anonymous:
        return queryset.none()

    return queryset.filter(
        id__in=ThreadParticipant.objects.filter(user=permissions.user).values(
            "thread_id"
        )
    )


def filter_private_thread_posts_queryset(
    permissions: UserPermissionsProxy,
    thread: Thread,
    queryset: QuerySet,
) -> QuerySet:
    return filter_private_thread_posts_queryset_hook(
        _filter_private_thread_posts_queryset_action, permissions, thread, queryset
    )


def _filter_private_thread_posts_queryset_action(
    permissions: UserPermissionsProxy,
    thread: Thread,
    queryset: QuerySet,
) -> QuerySet:
    return queryset
