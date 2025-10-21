from typing import TYPE_CHECKING

from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404, HttpRequest
from django.utils.translation import pgettext_lazy

from ..permissions.privatethreads import (
    check_private_threads_permission,
    check_start_private_threads_permission,
)
from ..permissions.proxy import UserPermissionsProxy
from ..users.bans import get_user_ban
from .hooks import (
    validate_new_private_thread_member_hook,
    validate_new_private_thread_owner_hook,
)

if TYPE_CHECKING:
    from ..users.models import User


def validate_new_private_thread_owner(
    new_owner_permissions: UserPermissionsProxy,
    user_permissions: UserPermissionsProxy,
    cache_versions: dict,
    request: HttpRequest | None = None,
):
    validate_new_private_thread_owner_hook(
        _validate_new_private_thread_owner_action,
        new_owner_permissions,
        user_permissions,
        cache_versions,
        request,
    )


def _validate_new_private_thread_owner_action(
    new_owner_permissions: UserPermissionsProxy,
    user_permissions: UserPermissionsProxy,
    cache_versions: dict,
    request: HttpRequest | None = None,
):
    user = new_owner_permissions.user

    if get_user_ban(user, cache_versions):
        raise ValidationError(
            pgettext_lazy("new private thread owner validator", "This user is banned."),
            code="banned",
        )

    try:
        check_private_threads_permission(new_owner_permissions)
    except (Http404, PermissionDenied):
        raise ValidationError(
            pgettext_lazy(
                "new private thread owner validator",
                "This user can't use private threads.",
            ),
            code="permission_denied",
        )

    try:
        check_start_private_threads_permission(new_owner_permissions)
    except (Http404, PermissionDenied):
        raise ValidationError(
            pgettext_lazy(
                "new private thread owner validator",
                "This user can't own private threads.",
            ),
            code="permission_denied",
        )


def validate_new_private_thread_member(
    new_member_permissions: UserPermissionsProxy,
    user_permissions: UserPermissionsProxy,
    cache_versions: dict,
    request: HttpRequest | None = None,
):
    validate_new_private_thread_member_hook(
        _validate_new_private_thread_member_action,
        new_member_permissions,
        user_permissions,
        cache_versions,
        request,
    )


def _validate_new_private_thread_member_action(
    new_member_permissions: UserPermissionsProxy,
    user_permissions: UserPermissionsProxy,
    cache_versions: dict,
    request: HttpRequest | None = None,
):
    user = new_member_permissions.user

    if get_user_ban(user, cache_versions):
        raise ValidationError(
            pgettext_lazy(
                "new private thread member validator", "This user is banned."
            ),
            code="banned",
        )

    try:
        check_private_threads_permission(new_member_permissions)
    except (Http404, PermissionDenied):
        raise ValidationError(
            pgettext_lazy(
                "new private thread member validator",
                "This user can't use private threads.",
            ),
            code="permission_denied",
        )

    if not _check_can_be_added_by_other_user(user, user_permissions):
        raise ValidationError(
            pgettext_lazy(
                "new private thread member validator",
                "This user limits who can add them to private threads.",
            ),
            code="limited",
        )


def _check_can_be_added_by_other_user(
    user: "User", user_permissions: UserPermissionsProxy
) -> bool:
    if user.can_be_messaged_by_everyone or user_permissions.is_global_moderator:
        return True

    if user.can_be_messaged_by_nobody:
        return False

    return user.is_following(user_permissions.user)
