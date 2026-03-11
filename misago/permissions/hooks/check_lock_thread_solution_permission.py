from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook
from ...threads.models import Thread

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class CheckLockThreadSolutionPermissionHookAction(Protocol):
    """
    Misago function used to check whether the user has permission to lock
    the thread’s selected solution. Raises `PermissionDenied` with an error
    message if they do not.

    # Arguments

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `thread: Thread`

    The thread to check permissions for.
    """

    def __call__(
        self,
        permissions: "UserPermissionsProxy",
        thread: Thread,
    ) -> None: ...


class CheckLockThreadSolutionPermissionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CheckLockThreadSolutionPermissionHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `thread: Thread`

    The thread to check permissions for.
    """

    def __call__(
        self,
        action: CheckLockThreadSolutionPermissionHookAction,
        permissions: "UserPermissionsProxy",
        thread: Thread,
    ) -> None: ...


class CheckLockThreadSolutionPermissionHook(
    FilterHook[
        CheckLockThreadSolutionPermissionHookAction,
        CheckLockThreadSolutionPermissionHookFilter,
    ]
):
    """
    This hook wraps the standard Misago function used to check whether the user
    has permission to lock the thread’s selected solution.
    Raises `PermissionDenied` with an error message if they do not.

    # Example

    The code below implements a custom filter function that allows user with
    the special "curator" flag to lock selected solution.

    ```python
    from misago.permissions.hooks import check_lock_thread_solution_permission_hook
    from misago.permissions.proxy import UserPermissionsProxy
    from misago.threads.models import Thread

    @check_lock_thread_solution_permission_hook.append_filter
    def check_lock_thread_solution_permission(
        action,
        permissions: UserPermissionsProxy,
        thread: Thread,
    ) -> None:
        if (
            permissions.user.is_authenticated
            and permissions.user.plugin_data.get("qa_curator")
        ):
            return

        # Run standard permission checks
        action(permissions, thread)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CheckLockThreadSolutionPermissionHookAction,
        permissions: "UserPermissionsProxy",
        thread: Thread,
    ) -> None:
        return super().__call__(action, permissions, thread)


check_lock_thread_solution_permission_hook = CheckLockThreadSolutionPermissionHook()
