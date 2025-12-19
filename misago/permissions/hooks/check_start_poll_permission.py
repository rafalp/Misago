from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class CheckStartPollPermissionHookAction(Protocol):
    """
    Misago function used to check if the user has permission to start
    polls. Raises Django's `PermissionDenied` with an error message if they don't.

    # Arguments

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.
    """

    def __call__(self, permissions: "UserPermissionsProxy") -> None: ...


class CheckStartPollPermissionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CheckStartPollPermissionHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.
    """

    def __call__(
        self,
        action: CheckStartPollPermissionHookAction,
        permissions: "UserPermissionsProxy",
    ) -> None: ...


class CheckStartPollPermissionHook(
    FilterHook[
        CheckStartPollPermissionHookAction,
        CheckStartPollPermissionHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the permission check for
    the "can start polls" permission.

    # Example

    Prevent a user from starting polls if their account is less than 30 days old.

    ```python
    from datetime import timedelta

    from django.core.exceptions import PermissionDenied
    from django.utils import timezone
    from django.utils.translation import pgettext
    from misago.permissions.hooks import check_start_poll_permission_hook
    from misago.permissions.proxy import UserPermissionsProxy

    @check_start_poll_permission_hook.append_filter
    def check_user_can_start_poll(
        action, permissions: UserPermissionsProxy
    ) -> None:
        # Run standard permission checks
        action(permissions)

        required_account_age = timezone.now() - timedelta(days=30)
        if permissions.user.joined_on > required_account_age:
            raise PermissionDenied(
                pgettext(
                    "poll permission error",
                    "Your account must be at least 30 days old before you can start polls."
                )
            )
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CheckStartPollPermissionHookAction,
        permissions: "UserPermissionsProxy",
    ) -> None:
        return super().__call__(action, permissions)


check_start_poll_permission_hook = CheckStartPollPermissionHook()
