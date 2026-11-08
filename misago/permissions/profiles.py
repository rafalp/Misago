from typing import TYPE_CHECKING

from django.core.exceptions import PermissionDenied
from django.utils.translation import pgettext

from .hooks import (
    check_see_user_profile_permission_hook,
)
from .proxy import UserPermissionsProxy

if TYPE_CHECKING:
    from ..users.models import User


def check_see_user_profile_permission(permissions: UserPermissionsProxy, user: "User"):
    check_see_user_profile_permission_hook(
        _check_see_user_profile_permission_action, permissions, user
    )


def _check_see_user_profile_permission_action(
    permissions: UserPermissionsProxy, user: "User"
):
    if permissions.user.is_authenticated and permissions.user.id == user.id:
        return

    if not permissions.can_see_user_profiles:
        raise PermissionDenied(
            pgettext(
                "user profile permission error",
                "You can't view user profiles.",
            )
        )
