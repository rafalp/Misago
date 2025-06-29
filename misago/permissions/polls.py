from django.core.exceptions import PermissionDenied
from django.utils.translation import pgettext

from .hooks import check_start_poll_permission_hook
from .proxy import UserPermissionsProxy


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
