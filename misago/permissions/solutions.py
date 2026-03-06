from math import ceil

from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.utils.translation import npgettext, pgettext

from ..threads.models import Post, Thread
from .hooks import (
    check_change_thread_solution_permission_hook,
    check_clear_thread_solution_permission_hook,
    check_select_thread_solution_permission_hook,
)
from .proxy import UserPermissionsProxy
from .threads import (
    check_locked_category_permission,
    check_locked_thread_permission,
)


def check_select_thread_solution_permission(
    permissions: UserPermissionsProxy, post: Post
):
    check_select_thread_solution_permission_hook(
        _check_select_thread_solution_permission_action,
        permissions,
        post,
    )


def _check_select_thread_solution_permission_action(
    permissions: UserPermissionsProxy, post: Post
):
    if not post.category.enable_solutions:
        raise PermissionDenied(
            pgettext(
                "solutions permission error",
                "You can't select thread solutions in this category.",
            )
        )

    if permissions.is_category_moderator(post.category_id):
        return

    if (
        not permissions.user.is_authenticated
        or permissions.user.id != post.thread.starter_id
    ):
        raise PermissionDenied(
            pgettext(
                "solutions permission error",
                "You can't select thread solutions in other users' threads.",
            )
        )

    if not permissions.can_select_own_thread_solutions:
        raise PermissionDenied(
            pgettext(
                "solutions permission error",
                "You can't select thread solutions.",
            )
        )

    check_locked_category_permission(permissions, post.category)
    check_locked_thread_permission(permissions, post.thread)


def check_change_thread_solution_permission(
    permissions: UserPermissionsProxy, post: Post
):
    check_change_thread_solution_permission_hook(
        _check_change_thread_solution_permission_action,
        permissions,
        post,
    )


def _check_change_thread_solution_permission_action(
    permissions: UserPermissionsProxy, post: Post
):
    thread = post.thread

    is_moderator = permissions.is_category_moderator(thread.category_id)

    if not thread.category.enable_solutions and (
        not is_moderator or not thread.solution_id
    ):
        raise PermissionDenied(
            pgettext(
                "solutions permission error",
                "You can't change thread solutions in this category.",
            )
        )

    if is_moderator:
        return

    if (
        not permissions.user.is_authenticated
        or permissions.user.id != post.thread.starter_id
    ):
        raise PermissionDenied(
            pgettext(
                "solutions permission error",
                "You can't change thread solutions in other users' threads.",
            )
        )

    if not permissions.can_change_own_thread_solutions:
        raise PermissionDenied(
            pgettext(
                "solutions permission error",
                "You can't change thread solutions.",
            )
        )

    check_locked_category_permission(permissions, post.category)
    check_locked_thread_permission(permissions, post.thread)

    if thread.solution.is_protected:
        raise PermissionDenied(
            pgettext(
                "solutions permission error",
                "This thread's solution is locked.",
            )
        )

    time_limit = permissions.own_thread_solutions_change_time_limit * 60

    if (
        time_limit
        and (timezone.now() - thread.solution_selected_at).total_seconds() > time_limit
    ):
        if time_limit >= 86400:
            days = ceil(time_limit / 86400)
            raise PermissionDenied(
                npgettext(
                    "solutions permission error",
                    "You can't change solutions selected more than %(days)s day ago.",
                    "You can't change solutions selected more than %(days)s days ago.",
                    days,
                )
                % {"days": days}
            )

        if time_limit >= 90 * 60:
            hours = ceil(time_limit / 3600)
            raise PermissionDenied(
                npgettext(
                    "solutions permission error",
                    "You can't change solutions selected more than %(hours)s hour ago.",
                    "You can't change solutions selected more than %(hours)s hours ago.",
                    hours,
                )
                % {"hours": hours}
            )

        minutes = ceil(time_limit / 60)
        raise PermissionDenied(
            npgettext(
                "solutions permission error",
                "You can't change solutions selected more than %(minutes)s minute ago.",
                "You can't change solutions selected more than %(minutes)s minutes ago.",
                minutes,
            )
            % {"minutes": minutes}
        )


def check_clear_thread_solution_permission(
    permissions: UserPermissionsProxy, thread: Thread
):
    check_clear_thread_solution_permission_hook(
        _check_clear_thread_solution_permission_action,
        permissions,
        thread,
    )


def _check_clear_thread_solution_permission_action(
    permissions: UserPermissionsProxy, thread: Thread
):
    is_moderator = permissions.is_category_moderator(thread.category_id)

    if not thread.category.enable_solutions and (
        not is_moderator or not thread.solution_id
    ):
        raise PermissionDenied(
            pgettext(
                "solutions permission error",
                "You can't clear thread solutions in this category.",
            )
        )

    if is_moderator:
        return

    if (
        not permissions.user.is_authenticated
        or permissions.user.id != thread.starter_id
    ):
        raise PermissionDenied(
            pgettext(
                "solutions permission error",
                "You can't clear thread solutions in other users' threads.",
            )
        )

    if not permissions.can_clear_own_thread_solutions:
        raise PermissionDenied(
            pgettext(
                "solutions permission error",
                "You can't clear thread solutions",
            )
        )

    check_locked_category_permission(permissions, thread.category)
    check_locked_thread_permission(permissions, thread)

    if thread.solution.is_protected:
        raise PermissionDenied(
            pgettext(
                "solutions permission error",
                "This thread's solution is locked.",
            )
        )

    time_limit = permissions.own_thread_solutions_clear_time_limit * 60

    if (
        time_limit
        and (timezone.now() - thread.solution_selected_at).total_seconds() > time_limit
    ):
        if time_limit >= 86400:
            days = ceil(time_limit / 86400)
            raise PermissionDenied(
                npgettext(
                    "solutions permission error",
                    "You can't clear solutions selected more than %(days)s day ago.",
                    "You can't clear solutions selected more than %(days)s days ago.",
                    days,
                )
                % {"days": days}
            )

        if time_limit >= 90 * 60:
            hours = ceil(time_limit / 3600)
            raise PermissionDenied(
                npgettext(
                    "solutions permission error",
                    "You can't clear solutions selected more than %(hours)s hour ago.",
                    "You can't clear solutions selected more than %(hours)s hours ago.",
                    hours,
                )
                % {"hours": hours}
            )

        minutes = ceil(time_limit / 60)
        raise PermissionDenied(
            npgettext(
                "solutions permission error",
                "You can't clear solutions selected more than %(minutes)s minute ago.",
                "You can't clear solutions selected more than %(minutes)s minutes ago.",
                minutes,
            )
            % {"minutes": minutes}
        )
