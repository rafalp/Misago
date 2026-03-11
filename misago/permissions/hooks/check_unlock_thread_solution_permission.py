from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook
from ...threads.models import Thread

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class CheckUnlockThreadSolutionPermissionHookAction(Protocol):
    """
    Misago function used to check whether the user has permission to unlock
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


class CheckUnlockThreadSolutionPermissionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CheckUnlockThreadSolutionPermissionHookAction`

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
        action: CheckUnlockThreadSolutionPermissionHookAction,
        permissions: "UserPermissionsProxy",
        thread: Thread,
    ) -> None: ...


class CheckUnlockThreadSolutionPermissionHook(
    FilterHook[
        CheckUnlockThreadSolutionPermissionHookAction,
        CheckUnlockThreadSolutionPermissionHookFilter,
    ]
):
    """
    This hook wraps the standard Misago function used to check whether the user
    has permission to unlock the thread’s selected solution.
    Raises `PermissionDenied` with an error message if they do not.

    # Example

    The code below implements a custom filter function that allows user with
    the special "curator" flag to unlock selected solution if it was locked
    by them.

    ```python
    from misago.permissions.hooks import check_unlock_thread_solution_permission_hook
    from misago.permissions.proxy import UserPermissionsProxy
    from misago.threads.models import Thread

    @check_unlock_thread_solution_permission_hook.append_filter
    def check_unlock_thread_solution_permission(
        action,
        permissions: UserPermissionsProxy,
        thread: Thread,
    ) -> None:
        if (
            permissions.user.is_authenticated
            and permissions.user.plugin_data.get("qa_curator")
            and thread.solution_locked_by_id == permissions.user.id
        ):
            return

        # Run standard permission checks
        action(permissions, thread)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CheckUnlockThreadSolutionPermissionHookAction,
        permissions: "UserPermissionsProxy",
        thread: Thread,
    ) -> None:
        return super().__call__(action, permissions, thread)


check_unlock_thread_solution_permission_hook = CheckUnlockThreadSolutionPermissionHook()
