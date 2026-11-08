from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class CheckSearchUsersPermissionHookAction(Protocol):
    """
    Misago function used to check if the user has permission to search for users.
    Raises Django's `PermissionDenied` with an error message if they don't.

    # Arguments

    ## `permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.
    """

    def __call__(
        self,
        permissions: "UserPermissionsProxy",
    ) -> None: ...


class CheckSearchUsersPermissionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CheckSearchUsersPermissionHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.
    """

    def __call__(
        self,
        action: CheckSearchUsersPermissionHookAction,
        permissions: "UserPermissionsProxy",
    ) -> None: ...


class CheckSearchUsersPermissionHook(
    FilterHook[
        CheckSearchUsersPermissionHookAction,
        CheckSearchUsersPermissionHookFilter,
    ]
):
    """
    This hook wraps a Misago function used to check if a user has permission to
    search for users. Raises Django's `PermissionDenied` with an error message
    if they don't.

    # Example

    The code below implements a custom filter function that blocks user from
    searching for users if their IP address is banned.

    ```python
    from django.core.exceptions import PermissionDenied
    from django.utils.translation import pgettext
    from misago.users.bans import get_request_ip_ban
    from misago.permissions.hooks import check_search_users_permission_hook
    from misago.permissions.proxy import UserPermissionsProxy

    @check_search_users_permission_hook.append_filter
    def check_user_can_search_users_permission(
        action,
        permissions: UserPermissionsProxy,
    ) -> None:
        # Run standard permission checks
        action(permissions)

        if get_request_ip_ban(request):
            raise PermissionDenied(
                pgettext(
                    "search permission error",
                    "You can't search for users."
                )
            )
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CheckSearchUsersPermissionHookAction,
        permissions: "UserPermissionsProxy",
    ) -> None:
        return super().__call__(action, permissions)


check_search_users_permission_hook = CheckSearchUsersPermissionHook()
