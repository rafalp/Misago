from math import ceil

from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils import timezone
from django.utils.translation import npgettext, pgettext

from ...categories.models import Category
from ...threads.models import Post, Thread
from ..categories import check_see_category_permission
from ..enums import CategoryPermission
from ..hooks import (
    check_edit_thread_permission_hook,
    check_edit_thread_post_permission_hook,
    check_locked_category_permission_hook,
    check_locked_thread_permission_hook,
    check_reply_thread_permission_hook,
    check_see_thread_permission_hook,
    check_see_thread_post_permission_hook,
    check_start_thread_permission_hook,
)
from ..proxy import UserPermissionsProxy


def check_locked_category_permission(
    permissions: UserPermissionsProxy, category: Category
):
    check_locked_category_permission_hook(
        _check_locked_category_permission_action,
        permissions,
        category,
    )


def _check_locked_category_permission_action(
    permissions: UserPermissionsProxy, category: Category
):
    if category.is_closed and not permissions.is_category_moderator(category.id):
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "This category is closed.",
            )
        )


def check_locked_thread_permission(permissions: UserPermissionsProxy, thread: Thread):
    check_locked_thread_permission_hook(
        _check_locked_thread_permission_action,
        permissions,
        thread,
    )


def _check_locked_thread_permission_action(
    permissions: UserPermissionsProxy, thread: Thread
):
    if thread.is_closed and not permissions.is_category_moderator(thread.category_id):
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "This thread is locked.",
            )
        )


def check_start_thread_permission(
    permissions: UserPermissionsProxy, category: Category
):
    check_start_thread_permission_hook(
        _check_start_thread_permission_action,
        permissions,
        category,
    )


def _check_start_thread_permission_action(
    permissions: UserPermissionsProxy, category: Category
):
    if category.id not in permissions.categories[CategoryPermission.START]:
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "You can't start new threads in this category.",
            )
        )

    check_locked_category_permission(permissions, category)


def check_see_thread_permission(
    permissions: UserPermissionsProxy, category: Category, thread: Thread
):
    check_see_thread_permission_hook(
        _check_see_thread_permission_action, permissions, category, thread
    )


def _check_see_thread_permission_action(
    permissions: UserPermissionsProxy, category: Category, thread: Thread
):
    if not permissions.is_category_moderator(category.id):
        if thread.is_hidden:
            raise Http404()

        if thread.is_unapproved and (
            thread.starter_id is None
            or permissions.user.is_anonymous
            or thread.starter_id != permissions.user.id
        ):
            raise Http404()

        if (
            category.show_started_only
            and not thread.weight
            and (
                thread.starter_id is None
                or permissions.user.is_anonymous
                or thread.starter_id != permissions.user.id
            )
        ):
            raise Http404()

    check_see_category_permission(permissions, category)

    if category.id not in permissions.categories[CategoryPermission.BROWSE]:
        if category.delay_browse_check:
            raise PermissionDenied(
                pgettext(
                    "category permission error",
                    "You can't browse the contents of this category.",
                )
            )

        raise Http404()


def check_reply_thread_permission(
    permissions: UserPermissionsProxy, category: Category, thread: Thread
):
    check_reply_thread_permission_hook(
        _check_reply_thread_permission_action, permissions, category, thread
    )


def _check_reply_thread_permission_action(
    permissions: UserPermissionsProxy, category: Category, thread: Thread
):
    if category.id not in permissions.categories[CategoryPermission.REPLY]:
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "You can't reply to threads in this category.",
            )
        )

    check_locked_category_permission(permissions, category)
    check_locked_thread_permission(permissions, thread)


def check_edit_thread_permission(
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
):
    check_edit_thread_permission_hook(
        _check_edit_thread_permission_action, permissions, category, thread
    )


def _check_edit_thread_permission_action(
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
):
    if category.id not in permissions.categories[CategoryPermission.START]:
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "You can't edit threads in this category.",
            )
        )

    check_locked_category_permission(permissions, category)
    check_locked_thread_permission(permissions, thread)

    if permissions.is_category_moderator(thread.category_id):
        return

    user_id = permissions.user.id
    is_starter = user_id and thread.starter_id and thread.starter_id == user_id

    if not is_starter:
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "You can't edit other users' threads.",
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

    if time_limit and (timezone.now() - thread.started_at).total_seconds() > time_limit:
        if time_limit >= 86400:
            days = ceil(time_limit / 86400)
            raise PermissionDenied(
                npgettext(
                    "threads permission error",
                    "You can't edit threads older than %(days)s day.",
                    "You can't edit threads older than %(days)s days.",
                    days,
                )
                % {"days": days}
            )

        if time_limit >= 90 * 60:
            hours = ceil(time_limit / 3600)
            raise PermissionDenied(
                npgettext(
                    "threads permission error",
                    "You can't edit threads older than %(hours)s hour.",
                    "You can't edit threads older than %(hours)s hours.",
                    hours,
                )
                % {"hours": hours}
            )

        minutes = ceil(time_limit / 60)
        raise PermissionDenied(
            npgettext(
                "threads permission error",
                "You can't edit threads older than %(minutes)s minute.",
                "You can't edit threads older than %(minutes)s minutes.",
                minutes,
            )
            % {"minutes": minutes}
        )


def check_see_thread_post_permission(
    permissions: UserPermissionsProxy, category: Category, thread: Thread, post: Post
):
    check_see_thread_post_permission_hook(
        _check_see_thread_post_permission_action, permissions, category, thread, post
    )


def _check_see_thread_post_permission_action(
    permissions: UserPermissionsProxy, category: Category, thread: Thread, post: Post
):
    if not permissions.is_category_moderator(category.id):
        if post.is_unapproved and (
            post.poster_id is None
            or permissions.user.is_anonymous
            or post.poster_id != permissions.user.id
        ):
            raise Http404()

        if post.is_hidden:
            raise PermissionDenied(
                pgettext(
                    "threads permission error",
                    "You can't see this post's contents.",
                )
            )


def check_edit_thread_post_permission(
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
    post: Post,
):
    check_edit_thread_post_permission_hook(
        _check_edit_thread_post_permission_action, permissions, category, thread, post
    )


def _check_edit_thread_post_permission_action(
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
    post: Post,
):
    if category.id not in permissions.categories[CategoryPermission.REPLY]:
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "You can't edit posts in this category.",
            )
        )

    check_locked_category_permission(permissions, category)
    check_locked_thread_permission(permissions, thread)

    if permissions.is_category_moderator(thread.category_id):
        return

    user_id = permissions.user.id
    is_poster = user_id and post.poster_id and post.poster_id == user_id

    if not is_poster:
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "You can't edit other users' posts.",
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

    if time_limit and (timezone.now() - post.posted_at).total_seconds() > time_limit:
        if time_limit >= 86400:
            days = ceil(time_limit / 86400)
            raise PermissionDenied(
                npgettext(
                    "threads permission error",
                    "You can't edit posts older than %(days)s day.",
                    "You can't edit posts older than %(days)s days.",
                    days,
                )
                % {"days": days}
            )

        if time_limit >= 90 * 60:
            hours = ceil(time_limit / 3600)
            raise PermissionDenied(
                npgettext(
                    "threads permission error",
                    "You can't edit posts older than %(hours)s hour.",
                    "You can't edit posts older than %(hours)s hours.",
                    hours,
                )
                % {"hours": hours}
            )

        minutes = ceil(time_limit / 60)
        raise PermissionDenied(
            npgettext(
                "threads permission error",
                "You can't edit posts older than %(minutes)s minute.",
                "You can't edit posts older than %(minutes)s minutes.",
                minutes,
            )
            % {"minutes": minutes}
        )
