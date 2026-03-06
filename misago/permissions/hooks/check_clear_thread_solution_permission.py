from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook
from ...threads.models import Thread

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class CheckClearThreadSolutionPermissionHookAction(Protocol):
    """
    Misago function used to check whether the user has permission to clear
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


class CheckClearThreadSolutionPermissionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CheckClearThreadSolutionPermissionHookAction`

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
        action: CheckClearThreadSolutionPermissionHookAction,
        permissions: "UserPermissionsProxy",
        thread: Thread,
    ) -> None: ...


class CheckClearThreadSolutionPermissionHook(
    FilterHook[
        CheckClearThreadSolutionPermissionHookAction,
        CheckClearThreadSolutionPermissionHookFilter,
    ]
):
    """
    This hook wraps the standard Misago function used to check whether the user
    has permission to clear the thread’s selected solution.
    Raises `PermissionDenied` with an error message if they do not.

    # Example

    The code below implements a custom filter function that blocks a user from
    clearing a thread’s solution unless they were the one who selected it.

    ```python
    from django.core.exceptions import PermissionDenied
    from django.utils.translation import pgettext
    from misago.permissions.hooks import check_clear_thread_solution_permission_hook
    from misago.permissions.proxy import UserPermissionsProxy
    from misago.threads.models import Thread

    @check_clear_thread_solution_permission_hook.append_filter
    def check_clear_thread_solution_permission(
        action,
        permissions: UserPermissionsProxy,
        thread: Thread,
    ) -> None:
        # Run standard permission checks
        action(permissions, thread)

        if (
            not thread.solution_selected_by_id
            or thread.solution_selected_by_id != permissions.user.id
        ):
            raise PermissionDenied(
                pgettext(
                    "solutions permission error",
                    "You can't clear this thread's solution."
                )
            )
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CheckClearThreadSolutionPermissionHookAction,
        permissions: "UserPermissionsProxy",
        thread: Thread,
    ) -> None:
        return super().__call__(action, permissions, thread)


check_clear_thread_solution_permission_hook = CheckClearThreadSolutionPermissionHook()
