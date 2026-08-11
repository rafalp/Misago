from django.core.exceptions import PermissionDenied
from django.utils.translation import pgettext

from .hooks import check_search_permission_hook
from .proxy import UserPermissionsProxy


def check_search_permission(permissions: UserPermissionsProxy):
    check_search_permission_hook(_check_search_permission_action, permissions)


def _check_search_permission_action(permissions: UserPermissionsProxy):
    if not permissions.can_search:
        raise PermissionDenied(
            pgettext(
                "search permission error",
                "You can't search this site.",
            )
        )
