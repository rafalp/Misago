from math import ceil

from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.utils.translation import npgettext, pgettext

from ..categories.enums import CategoryTree
from ..categories.models import Category
from ..edits.models import PostEdit
from ..threads.models import Post, Thread
from .enums import CanHideOwnPostEdits, CanSeePostEdits
from .hooks import (
    can_see_post_edit_count_hook,
    check_delete_post_edit_permission_hook,
    check_hide_post_edit_permission_hook,
    check_restore_post_edit_permission_hook,
    check_see_post_edit_history_permission_hook,
    check_unhide_post_edit_permission_hook,
)
from .proxy import UserPermissionsProxy


def can_see_post_edit_count(
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
    post: Post,
) -> bool:
    return can_see_post_edit_count_hook(
        _can_see_post_edit_count_action, permissions, category, thread, post
    )


def _can_see_post_edit_count_action(
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
    post: Post,
) -> bool:
    is_user_post = permissions.user.id and permissions.user.id == post.poster_id
    return is_user_post or permissions.can_see_others_post_edits


def check_see_post_edit_history_permission(
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
    post: Post,
):
    check_see_post_edit_history_permission_hook(
        _check_see_post_edit_history_permission_action,
        permissions,
        category,
        thread,
        post,
    )


def _check_see_post_edit_history_permission_action(
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
    post: Post,
):
    is_user_post = permissions.user.id and permissions.user.id == post.poster_id

    if (
        not is_user_post
        and permissions.can_see_others_post_edits != CanSeePostEdits.HISTORY
    ):
        raise PermissionDenied(
            pgettext(
                "edits permission error",
                "You can’t see this post’s edit history.",
            )
        )


def check_restore_post_edit_permission(
    permissions: UserPermissionsProxy, post_edit: PostEdit
):
    check_restore_post_edit_permission_hook(
        _check_restore_post_edit_permission_action,
        permissions,
        post_edit,
    )


def _check_restore_post_edit_permission_action(
    permissions: UserPermissionsProxy, post_edit: PostEdit
):
    if not post_edit.old_content:
        raise PermissionDenied(
            pgettext(
                "edits permission error",
                "You can’t restore the post from this edit.",
            )
        )

    if permissions.is_global_moderator:
        return

    category = post_edit.category

    if category.tree_id == CategoryTree.THREADS and permissions.is_category_moderator(
        category.id
    ):
        return

    if (
        category.tree_id == CategoryTree.PRIVATE_THREADS
        and permissions.is_private_threads_moderator
    ):
        return

    if post_edit.is_hidden:
        raise PermissionDenied(
            pgettext(
                "edits permission error",
                "You can’t restore the post from hidden edit.",
            )
        )


def check_hide_post_edit_permission(
    permissions: UserPermissionsProxy, post_edit: PostEdit
):
    check_hide_post_edit_permission_hook(
        _check_hide_post_edit_permission_action,
        permissions,
        post_edit,
    )


def _check_hide_post_edit_permission_action(
    permissions: UserPermissionsProxy,
    post_edit: PostEdit,
):
    if permissions.is_global_moderator:
        return

    category = post_edit.category

    if category.tree_id == CategoryTree.THREADS and permissions.is_category_moderator(
        category.id
    ):
        return

    if (
        category.tree_id == CategoryTree.PRIVATE_THREADS
        and permissions.is_private_threads_moderator
    ):
        return

    is_user_edit = permissions.user.id and permissions.user.id == post_edit.user_id
    if not is_user_edit:
        raise PermissionDenied(
            pgettext(
                "edits permission error",
                "You can’t hide post edits made by other users.",
            )
        )

    if not permissions.can_hide_own_post_edits:
        raise PermissionDenied(
            pgettext(
                "edits permission error",
                "You can’t hide post edits.",
            )
        )

    time_limit = permissions.own_post_edits_hide_time_limit * 60

    if (
        time_limit
        and (timezone.now() - post_edit.edited_at).total_seconds() > time_limit
    ):
        if time_limit >= 86400:
            days = ceil(time_limit / 86400)
            raise PermissionDenied(
                npgettext(
                    "edits permission error",
                    "You can't hide post edits older than %(days)s day.",
                    "You can't hide post edits older than %(days)s days.",
                    days,
                )
                % {"days": days}
            )

        if time_limit >= 90 * 60:
            hours = ceil(time_limit / 3600)
            raise PermissionDenied(
                npgettext(
                    "edits permission error",
                    "You can't hide post edits older than %(hours)s hour.",
                    "You can't hide post edits older than %(hours)s hours.",
                    hours,
                )
                % {"hours": hours}
            )

        minutes = ceil(time_limit / 60)
        raise PermissionDenied(
            npgettext(
                "edits permission error",
                "You can't hide post edits older than %(minutes)s minute.",
                "You can't hide post edits older than %(minutes)s minutes.",
                minutes,
            )
            % {"minutes": minutes}
        )


def check_unhide_post_edit_permission(
    permissions: UserPermissionsProxy, post_edit: PostEdit
):
    check_unhide_post_edit_permission_hook(
        _check_unhide_post_edit_permission_action,
        permissions,
        post_edit,
    )


def _check_unhide_post_edit_permission_action(
    permissions: UserPermissionsProxy,
    post_edit: PostEdit,
):
    if permissions.is_global_moderator:
        return

    category = post_edit.category

    if category.tree_id == CategoryTree.THREADS and permissions.is_category_moderator(
        category.id
    ):
        return

    if (
        category.tree_id == CategoryTree.PRIVATE_THREADS
        and permissions.is_private_threads_moderator
    ):
        return

    raise PermissionDenied(
        pgettext(
            "edits permission error",
            "You can’t unhide hidden post edits.",
        )
    )


def check_delete_post_edit_permission(
    permissions: UserPermissionsProxy, post_edit: PostEdit
):
    check_delete_post_edit_permission_hook(
        _check_delete_post_edit_permission_action,
        permissions,
        post_edit,
    )


def _check_delete_post_edit_permission_action(
    permissions: UserPermissionsProxy,
    post_edit: PostEdit,
):
    if permissions.is_global_moderator:
        return

    category = post_edit.category

    if category.tree_id == CategoryTree.THREADS and permissions.is_category_moderator(
        category.id
    ):
        return

    if (
        category.tree_id == CategoryTree.PRIVATE_THREADS
        and permissions.is_private_threads_moderator
    ):
        return

    is_user_edit = permissions.user.id and permissions.user.id == post_edit.user_id

    if not is_user_edit:
        raise PermissionDenied(
            pgettext(
                "edits permission error",
                "You can’t delete post edits made by other users.",
            )
        )

    if permissions.can_hide_own_post_edits != CanHideOwnPostEdits.DELETE:
        raise PermissionDenied(
            pgettext(
                "edits permission error",
                "You can’t delete post edits.",
            )
        )

    if post_edit.is_hidden and permissions.user.id != post_edit.hidden_by_id:
        raise PermissionDenied(
            pgettext(
                "edits permission error",
                "You can’t delete post edits hidden by other users.",
            )
        )

    time_limit = permissions.own_post_edits_hide_time_limit * 60

    if (
        time_limit
        and (timezone.now() - post_edit.edited_at).total_seconds() > time_limit
    ):
        if time_limit >= 86400:
            days = ceil(time_limit / 86400)
            raise PermissionDenied(
                npgettext(
                    "edits permission error",
                    "You can't delete post edits older than %(days)s day.",
                    "You can't delete post edits older than %(days)s days.",
                    days,
                )
                % {"days": days}
            )

        if time_limit >= 90 * 60:
            hours = ceil(time_limit / 3600)
            raise PermissionDenied(
                npgettext(
                    "edits permission error",
                    "You can't delete post edits older than %(hours)s hour.",
                    "You can't delete post edits older than %(hours)s hours.",
                    hours,
                )
                % {"hours": hours}
            )

        minutes = ceil(time_limit / 60)
        raise PermissionDenied(
            npgettext(
                "edits permission error",
                "You can't delete post edits older than %(minutes)s minute.",
                "You can't delete post edits older than %(minutes)s minutes.",
                minutes,
            )
            % {"minutes": minutes}
        )
