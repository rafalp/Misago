from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook
from ...threads.models import Thread

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class CheckChangePrivateThreadOwnerPermissionHookAction(Protocol):
    """
    Misago function that checks whether a user has permission to change
    a private thread's owner. Raises `PermissionDenied` if they don't.

    # Arguments

    ## `permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `thread: Thread`

    The thread to check permissions for.
    """

    def __call__(
        self,
        permissions: "UserPermissionsProxy",
        thread: Thread,
    ) -> None: ...


class CheckChangePrivateThreadOwnerPermissionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CheckChangePrivateThreadOwnerPermissionHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    ## `permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `thread: Thread`

    The thread to check permissions for.
    """

    def __call__(
        self,
        action: CheckChangePrivateThreadOwnerPermissionHookAction,
        permissions: "UserPermissionsProxy",
        thread: Thread,
    ) -> None: ...


class CheckChangePrivateThreadOwnerPermissionHook(
    FilterHook[
        CheckChangePrivateThreadOwnerPermissionHookAction,
        CheckChangePrivateThreadOwnerPermissionHookFilter,
    ]
):
    """
    This hook allows plugins to extend or replace the logic for checking whether
    a user has permission to change a private thread's owner.

    # Example

    Prevent a user flagged as a support employee from giving away
    ownership of a private thread:

    ```python
    from django.core.exceptions import PermissionDenied
    from misago.permissions.hooks import check_change_private_thread_owner_permission_hook
    from misago.permissions.proxy import UserPermissionsProxy
    from misago.threads.models import Thread

    @check_change_private_thread_owner_permission_hook.append_filter
    def check_user_can_change_private_thread_owner(
        action,
        permissions: UserPermissionsProxy,
        thread: Thread,
    ) -> None:
        # Run default checks
        action(permissions, thread)

        if (
            not permissions.is_private_threads_moderator
            and permissions.user.plugin_data["support"]
        ):
            raise PermissionDenied("You cant give away a private thread ownership.")
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CheckChangePrivateThreadOwnerPermissionHookAction,
        permissions: "UserPermissionsProxy",
        thread: Thread,
    ) -> None:
        return super().__call__(action, permissions, thread)


check_change_private_thread_owner_permission_hook = (
    CheckChangePrivateThreadOwnerPermissionHook()
)
