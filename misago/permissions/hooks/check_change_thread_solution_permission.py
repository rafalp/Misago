from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook
from ...threads.models import Post

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class CheckChangeThreadSolutionPermissionHookAction(Protocol):
    """
    Misago function used to check whether the user has permission to change
    the thread’s solution to a new post. Raises `PermissionDenied` with an error
    message if they don't.

    # Arguments

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `post: Post`

    The post to check permissions for.
    """

    def __call__(
        self,
        permissions: "UserPermissionsProxy",
        post: Post,
    ) -> None: ...


class CheckChangeThreadSolutionPermissionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CheckChangeThreadSolutionPermissionHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `post: Post`

    The post to check permissions for.
    """

    def __call__(
        self,
        action: CheckChangeThreadSolutionPermissionHookAction,
        permissions: "UserPermissionsProxy",
        post: Post,
    ) -> None: ...


class CheckChangeThreadSolutionPermissionHook(
    FilterHook[
        CheckChangeThreadSolutionPermissionHookAction,
        CheckChangeThreadSolutionPermissionHookFilter,
    ]
):
    """
    This hook wraps the standard Misago function used to check whether the user
    has permission to change the thread’s solution to a new post.
    Raises `PermissionDenied` with an error message if they don't.

    # Example

    The code below implements a custom filter function that blocks a user from
    changing a thread's solution if it wasn't selected by them.

    ```python
    from django.core.exceptions import PermissionDenied
    from django.utils.translation import pgettext
    from misago.permissions.hooks import check_change_thread_solution_permission_hook
    from misago.permissions.proxy import UserPermissionsProxy
    from misago.threads.models import Post

    @check_change_thread_solution_permission_hook.append_filter
    def check_change_thread_solution_permission(
        action,
        permissions: UserPermissionsProxy,
        post: Post,
    ) -> None:
        # Run standard permission checks
        action(permissions, post)

        if post.thread.solution_selected_by_id != permissions.user.id:
            raise PermissionDenied(
                pgettext(
                    "solutions permission error",
                    "This thread’s solution can't be changed."
                )
            )
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CheckChangeThreadSolutionPermissionHookAction,
        permissions: "UserPermissionsProxy",
        post: Post,
    ) -> None:
        return super().__call__(action, permissions, post)


check_change_thread_solution_permission_hook = CheckChangeThreadSolutionPermissionHook()
