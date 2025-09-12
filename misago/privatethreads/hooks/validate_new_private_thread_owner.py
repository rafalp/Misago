from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ...permissions.proxy import UserPermissionsProxy


class ValidateNewPrivateThreadOwnerHookAction(Protocol):
    """
    Misago function that validates a new private thread owner.

    # Arguments

    ## `new_owner_permissions: UserPermissionsProxy`

    A proxy object with the new owner's permissions.

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `cache_versions: dict`

    A Python `dict` with cache versions.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.
    """

    def __call__(
        self,
        new_owner_permissions: "UserPermissionsProxy",
        user_permissions: "UserPermissionsProxy",
        cache_versions: dict,
        request: HttpRequest | None = None,
    ): ...


class ValidateNewPrivateThreadOwnerHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: ValidateNewPrivateThreadOwnerHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `new_owner_permissions: UserPermissionsProxy`

    A proxy object with the new owner's permissions.

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `cache_versions: dict`

    A Python `dict` with cache versions.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.
    """

    def __call__(
        self,
        action: ValidateNewPrivateThreadOwnerHookAction,
        new_owner_permissions: "UserPermissionsProxy",
        user_permissions: "UserPermissionsProxy",
        cache_versions: dict,
        request: HttpRequest | None = None,
    ): ...


class ValidateNewPrivateThreadOwnerHook(
    FilterHook[
        ValidateNewPrivateThreadOwnerHookAction,
        ValidateNewPrivateThreadOwnerHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the standard logic for
    validating new private thread owners.

    # Example

    Prevent a user from changing a private thread owner to someone whose account
    is less than five days old:

    ```python
    from django.core.exceptions import ValidationError
    from django.http import HttpRequest
    from django.utils import timezone
    from misago.permissions.proxy import UserPermissionsProxy
    from misago.privatethreads.hooks import validate_new_private_thread_owner_hook


    @validate_new_private_thread_owner_hook.append_filter
    def validate_new_private_thread_owner_registration_date(
        action,
        new_owner_permissions: UserPermissionsProxy,
        user_permissions: UserPermissionsProxy,
        cache_versions: dict,
        request: HttpRequest | None = None,
    ):
        action(
            new_owner_permissions,
            user_permissions,
            cache_versions,
            request,
        )

        new_owner_account_age = timezone.now() - new_owner_permissions.user.joined_on

        if new_owner_account_age.days < 5:
            raise ValidationError(
                "Cannot transfer ownership to a user under 5 days old."
            )
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: ValidateNewPrivateThreadOwnerHookAction,
        new_owner_permissions: "UserPermissionsProxy",
        user_permissions: "UserPermissionsProxy",
        cache_versions: dict,
        request: HttpRequest | None = None,
    ):
        return super().__call__(
            action,
            new_owner_permissions,
            user_permissions,
            cache_versions,
            request,
        )


validate_new_private_thread_owner_hook = ValidateNewPrivateThreadOwnerHook()
