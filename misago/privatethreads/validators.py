from typing import TYPE_CHECKING

from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404, HttpRequest
from django.utils.translation import pgettext_lazy

from ..permissions.privatethreads import check_private_threads_permission
from ..permissions.proxy import UserPermissionsProxy
from ..users.bans import get_user_ban

if TYPE_CHECKING:
    from ..users.models import User


def validate_can_invite_user(
    invited_user_permissions: UserPermissionsProxy,
    other_user_permissions: UserPermissionsProxy,
    cache_versions: dict,
    request: HttpRequest | None = None,
):
    _validate_can_invite_user_action(
        invited_user_permissions, other_user_permissions, cache_versions, request
    )


def _validate_can_invite_user_action(
    invited_user_permissions: UserPermissionsProxy,
    other_user_permissions: UserPermissionsProxy,
    cache_versions: dict,
    request: HttpRequest | None = None,
):
    user = invited_user_permissions.user

    if get_user_ban(user, cache_versions):
        raise ValidationError(
            pgettext_lazy("invite user validator", "This user is banned."),
            code="banned",
        )

    try:
        check_private_threads_permission(invited_user_permissions)
    except (Http404, PermissionDenied):
        raise ValidationError(
            pgettext_lazy(
                "invite user validator", "This user can't use private threads."
            ),
            code="permission_denied",
        )

    if not _check_can_be_invited_by_other_user(user, other_user_permissions):
        raise ValidationError(
            pgettext_lazy(
                "invite user validator",
                "This user limits who can invite them to private threads.",
            ),
            code="limited",
        )


def _check_can_be_invited_by_other_user(
    user: "User", other_user_permissions: UserPermissionsProxy
) -> bool:
    if user.can_be_messaged_by_everyone or other_user_permissions.is_global_moderator:
        return True

    if user.can_be_messaged_by_nobody:
        return False

    return user.is_following(other_user_permissions.user)
