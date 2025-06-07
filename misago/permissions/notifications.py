from django.core.exceptions import PermissionDenied
from django.utils.translation import pgettext

from .proxy import UserPermissionsProxy


def check_notifications_permission(permissions: UserPermissionsProxy):
    if permissions.user.is_anonymous:
        raise PermissionDenied(
            pgettext(
                "notifications permission error",
                "You must be signed in to access your notifications.",
            )
        )
