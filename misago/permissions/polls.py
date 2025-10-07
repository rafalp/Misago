from math import ceil

from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.utils.translation import npgettext, pgettext

from ..categories.models import Category
from ..polls.models import Poll
from ..threads.models import Thread
from .hooks import (
    check_close_thread_poll_permission_hook,
    check_delete_thread_poll_permission_hook,
    check_edit_thread_poll_permission_hook,
    check_open_thread_poll_permission_hook,
    check_start_poll_permission_hook,
    check_start_thread_poll_permission_hook,
    check_vote_in_thread_poll_permission_hook,
)
from .proxy import UserPermissionsProxy
from .threads import (
    check_locked_category_permission,
    check_locked_thread_permission,
)


def check_start_poll_permission(permissions: UserPermissionsProxy):
    check_start_poll_permission_hook(_check_start_poll_permission_action, permissions)


def _check_start_poll_permission_action(permissions: UserPermissionsProxy):
    if permissions.user.is_anonymous:
        raise PermissionDenied(
            pgettext(
                "polls permission error",
                "You must be signed in to start polls.",
            )
        )

    if not permissions.can_start_polls:
        raise PermissionDenied(
            pgettext(
                "polls permission error",
                "You can't start polls.",
            )
        )


def check_start_thread_poll_permission(
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
):
    check_start_thread_poll_permission_hook(
        _check_start_thread_poll_permission_action, permissions, category, thread
    )


def _check_start_thread_poll_permission_action(
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
):
    check_locked_category_permission(permissions, category)
    check_locked_thread_permission(permissions, thread)

    if thread.has_poll:
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "This thread already has a poll.",
            )
        )

    check_start_poll_permission(permissions)

    if permissions.is_category_moderator(thread.category_id):
        return

    user_id = permissions.user.id
    if not (user_id and thread.starter_id and thread.starter_id == user_id):
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "You can't start polls in other users' threads.",
            )
        )


def check_edit_thread_poll_permission(
    permissions: UserPermissionsProxy, category: Category, thread: Thread, poll: Poll
):
    check_edit_thread_poll_permission_hook(
        _check_edit_thread_poll_permission_action, permissions, category, thread, poll
    )


def _check_edit_thread_poll_permission_action(
    permissions: UserPermissionsProxy, category: Category, thread: Thread, poll: Poll
):
    check_locked_category_permission(permissions, category)
    check_locked_thread_permission(permissions, thread)

    if permissions.is_category_moderator(thread.category_id):
        return

    user_id = permissions.user.id
    if not (user_id and thread.starter_id and thread.starter_id == user_id):
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "You can't edit polls in other users' threads.",
            )
        )

    if not (user_id and poll.starter_id and poll.starter_id == user_id):
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "You can't edit other users' polls.",
            )
        )

    if not permissions.can_edit_own_polls:
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "You can't edit polls.",
            )
        )

    if poll.has_ended:
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "You can't edit polls that have ended.",
            )
        )

    if poll.is_closed:
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "You can't edit polls that are closed.",
            )
        )

    time_limit = permissions.own_polls_edit_time_limit * 60

    if time_limit and (timezone.now() - poll.started_at).total_seconds() > time_limit:
        if time_limit >= 86400:
            days = ceil(time_limit / 86400)
            raise PermissionDenied(
                npgettext(
                    "threads permission error",
                    "You can't edit polls older than %(days)s day.",
                    "You can't edit polls older than %(days)s days.",
                    days,
                )
                % {"days": days}
            )

        if time_limit >= 90 * 60:
            hours = ceil(time_limit / 3600)
            raise PermissionDenied(
                npgettext(
                    "threads permission error",
                    "You can't edit polls older than %(hours)s hour.",
                    "You can't edit polls older than %(hours)s hours.",
                    hours,
                )
                % {"hours": hours}
            )

        minutes = ceil(time_limit / 60)
        raise PermissionDenied(
            npgettext(
                "threads permission error",
                "You can't edit polls older than %(minutes)s minute.",
                "You can't edit polls older than %(minutes)s minutes.",
                minutes,
            )
            % {"minutes": minutes}
        )


def check_close_thread_poll_permission(
    permissions: UserPermissionsProxy, category: Category, thread: Thread, poll: Poll
):
    check_close_thread_poll_permission_hook(
        _check_close_thread_poll_permission_action, permissions, category, thread, poll
    )


def _check_close_thread_poll_permission_action(
    permissions: UserPermissionsProxy, category: Category, thread: Thread, poll: Poll
):
    check_locked_category_permission(permissions, category)
    check_locked_thread_permission(permissions, thread)

    if permissions.is_category_moderator(thread.category_id):
        return

    user_id = permissions.user.id
    if not (user_id and thread.starter_id and thread.starter_id == user_id):
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "You can't close polls in other users' threads.",
            )
        )

    if not (user_id and poll.starter_id and poll.starter_id == user_id):
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "You can't close other users' polls.",
            )
        )

    if not permissions.can_close_own_polls:
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "You can't close polls.",
            )
        )

    time_limit = permissions.own_polls_close_time_limit * 60
    if time_limit and (timezone.now() - poll.started_at).total_seconds() > time_limit:
        if time_limit >= 86400:
            days = ceil(time_limit / 86400)
            raise PermissionDenied(
                npgettext(
                    "threads permission error",
                    "You can't close polls older than %(days)s day.",
                    "You can't close polls older than %(days)s days.",
                    days,
                )
                % {"days": days}
            )

        if time_limit >= 90 * 60:
            hours = ceil(time_limit / 3600)
            raise PermissionDenied(
                npgettext(
                    "threads permission error",
                    "You can't close polls older than %(hours)s hour.",
                    "You can't close polls older than %(hours)s hours.",
                    hours,
                )
                % {"hours": hours}
            )

        minutes = ceil(time_limit / 60)
        raise PermissionDenied(
            npgettext(
                "threads permission error",
                "You can't close polls older than %(minutes)s minute.",
                "You can't close polls older than %(minutes)s minutes.",
                minutes,
            )
            % {"minutes": minutes}
        )


def check_open_thread_poll_permission(
    permissions: UserPermissionsProxy, category: Category, thread: Thread, poll: Poll
):
    check_open_thread_poll_permission_hook(
        _check_open_thread_poll_permission_action, permissions, category, thread, poll
    )


def _check_open_thread_poll_permission_action(
    permissions: UserPermissionsProxy, category: Category, thread: Thread, poll: Poll
):
    if permissions.is_category_moderator(thread.category_id):
        return

    raise PermissionDenied(
        pgettext(
            "threads permission error",
            "You can't open closed polls.",
        )
    )


def check_delete_thread_poll_permission(
    permissions: UserPermissionsProxy, category: Category, thread: Thread, poll: Poll
):
    check_delete_thread_poll_permission_hook(
        _check_delete_thread_poll_permission_action, permissions, category, thread, poll
    )


def _check_delete_thread_poll_permission_action(
    permissions: UserPermissionsProxy, category: Category, thread: Thread, poll: Poll
):
    if permissions.is_category_moderator(thread.category_id):
        return

    raise PermissionDenied(
        pgettext(
            "threads permission error",
            "You can't delete polls.",
        )
    )


def check_vote_in_thread_poll_permission(
    permissions: UserPermissionsProxy, category: Category, thread: Thread, poll: Poll
):
    check_vote_in_thread_poll_permission_hook(
        _check_vote_in_thread_poll_permission_action,
        permissions,
        category,
        thread,
        poll,
    )


def _check_vote_in_thread_poll_permission_action(
    permissions: UserPermissionsProxy, category: Category, thread: Thread, poll: Poll
):
    if permissions.user.is_anonymous:
        raise PermissionDenied(
            pgettext(
                "polls permission error",
                "You must be signed in to vote in polls.",
            )
        )

    if category.is_closed:
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "This category is locked.",
            )
        )

    if thread.is_closed:
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "This thread is locked.",
            )
        )

    if poll.has_ended:
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "This poll has ended.",
            )
        )

    if poll.is_closed:
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "This poll is closed.",
            )
        )

    if not permissions.can_vote_in_polls:
        raise PermissionDenied(
            pgettext(
                "threads permission error",
                "You can't vote in polls.",
            )
        )
