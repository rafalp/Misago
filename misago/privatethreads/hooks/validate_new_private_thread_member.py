from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ...permissions.proxy import UserPermissionsProxy


class ValidateNewPrivateThreadMemberHookAction(Protocol):
    """
    Misago function for validating new private thread members.

    # Arguments

    ## `new_member_permissions: UserPermissionsProxy`

    A proxy object with the invited user's permissions.

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `cache_versions: dict`

    A Python `dict` with cache versions.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.
    """

    def __call__(
        self,
        new_member_permissions: "UserPermissionsProxy",
        user_permissions: "UserPermissionsProxy",
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

    ## `new_member_permissions: UserPermissionsProxy`

    A proxy object with the invited user's permissions.

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `cache_versions: dict`

    A Python `dict` with cache versions.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.
    """

    def __call__(
        self,
        action: ValidateNewPrivateThreadMemberHookAction,
        new_member_permissions: "UserPermissionsProxy",
        user_permissions: "UserPermissionsProxy",
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

    Block new users from inviting non-staff users to their private threads:

    ```python
    from django.core.exceptions import ValidationError
    from django.http import HttpRequest
    from django.utils import timezone
    from misago.permissions.proxy import UserPermissionsProxy
    from misago.privatethreads.hooks import validate_new_private_thread_member_hook


    @validate_new_private_thread_member_hook.append_filter
    def validate_new_private_thread_member_registration_date(
        action,
        new_member_permissions: UserPermissionsProxy,
        user_permissions: UserPermissionsProxy,
        cache_versions: dict,
        request: HttpRequest | None = None,
    ):
        action(
            new_member_permissions,
            user_permissions,
            cache_versions,
            request,
        )

        user_is_new = (timezone.now() - user_permissions.user.joined_on).days < 7
        new_member_is_staff = (
            new_member_permissions.is_private_threads_moderator
            or new_member_permissions.moderated_categories
        )

        if user_is_new and not new_member_is_staff:
            raise ValidationError("Your account is less than 7 days old.")
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: ValidateNewPrivateThreadMemberHookAction,
        new_member_permissions: "UserPermissionsProxy",
        user_permissions: "UserPermissionsProxy",
        cache_versions: dict,
        request: HttpRequest | None = None,
    ):
        return super().__call__(
            action,
            new_member_permissions,
            user_permissions,
            cache_versions,
            request,
        )


validate_new_private_thread_member_hook = ValidateNewPrivateThreadMemberHook()
