from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ...permissions.proxy import UserPermissionsProxy


class ValidateNewPrivateThreadMemberHookAction(Protocol):
    """
    Misago function for validating new private thread members.

    # Arguments

    ## `invited_user_permissions: UserPermissionsProxy`

    A proxy object with the invited user's permissions.

    ## `other_user_permissions: UserPermissionsProxy`

    A proxy object with the inviting user's permissions.

    ## `cache_versions: dict`

    A Python `dict` with cache versions.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.
    """

    def __call__(
        self,
        invited_user_permissions: "UserPermissionsProxy",
        other_user_permissions: "UserPermissionsProxy",
        cache_versions: dict,
        request: HttpRequest | None = None,
    ): ...


class ValidateNewPrivateThreadMemberHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: ValidateNewPrivateThreadMemberHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `invited_user_permissions: UserPermissionsProxy`

    A proxy object with the invited user's permissions.

    ## `other_user_permissions: UserPermissionsProxy`

    A proxy object with the inviting user's permissions.

    ## `cache_versions: dict`

    A Python `dict` with cache versions.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.
    """

    def __call__(
        self,
        action: ValidateNewPrivateThreadMemberHookAction,
        invited_user_permissions: "UserPermissionsProxy",
        other_user_permissions: "UserPermissionsProxy",
        cache_versions: dict,
        request: HttpRequest | None = None,
    ): ...


class ValidateNewPrivateThreadMemberHook(
    FilterHook[
        ValidateNewPrivateThreadMemberHookAction,
        ValidateNewPrivateThreadMemberHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the standard logic for
    validating new private thread members.

    # Example

    Block new users from inviting non-staff users to their private threads.

    ```python
    from datetime import timedelta

    from django.core.exceptions import ValidationError
    from django.http import HttpRequest
    from django.utils import timezone
    from misago.permissions.proxy import UserPermissionsProxy
    from misago.privatethreads.hooks import validate_new_private_thread_member_hook


    @validate_new_private_thread_member_hook.append_filter
    def validate_new_private_thread_member_registration_date(
        action,
        invited_user_permissions: UserPermissionsProxy,
        other_user_permissions: UserPermissionsProxy,
        cache_versions: dict,
        request: HttpRequest | None = None,
    ):
        action(
            invited_user_permissions,
            other_user_permissions,
            cache_versions,
            request,
        )

        user_is_new = (timezone.now() - user.joined_on).days < 7

        if user_is_new and not invited_user_permissions.moderated_categories:
            raise ValidationError(
                "Your account is less than 7 days old."
            )
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: ValidateNewPrivateThreadMemberHookAction,
        invited_user_permissions: "UserPermissionsProxy",
        other_user_permissions: "UserPermissionsProxy",
        cache_versions: dict,
        request: HttpRequest | None = None,
    ):
        return super().__call__(
            action,
            invited_user_permissions,
            other_user_permissions,
            cache_versions,
            request,
        )


validate_new_private_thread_member_hook = ValidateNewPrivateThreadMemberHook()
