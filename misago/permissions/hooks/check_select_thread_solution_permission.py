from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook
from ...threads.models import Post

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class CheckSelectThreadSolutionPermissionHookAction(Protocol):
    """
    Misago function used to check whether the user has permission to select
    a post as the thread’s solution. Raises `PermissionDenied` with an error
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


class CheckSelectThreadSolutionPermissionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CheckSelectThreadSolutionPermissionHookAction`

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
        action: CheckSelectThreadSolutionPermissionHookAction,
        permissions: "UserPermissionsProxy",
        post: Post,
    ) -> None: ...


class CheckSelectThreadSolutionPermissionHook(
    FilterHook[
        CheckSelectThreadSolutionPermissionHookAction,
        CheckSelectThreadSolutionPermissionHookFilter,
    ]
):
    """
    This hook wraps a standard Misago function used to check whether the user
    has permission to select a post as the thread’s solution.
    Raises `PermissionDenied` with an error message if they don't.

    # Example

    The code below implements a custom filter function that blocks a user from
    selecting a post as a solution if it was posted by a shadow-banned user.

    ```python
    from django.core.exceptions import PermissionDenied
    from django.utils.translation import pgettext
    from misago.permissions.hooks import check_select_thread_solution_permission_hook
    from misago.permissions.proxy import UserPermissionsProxy
    from misago.threads.models import Post

    @check_select_thread_solution_permission_hook.append_filter
    def check_select_thread_solution_permission(
        action,
        permissions: UserPermissionsProxy,
        post: Post,
    ) -> None:
        # Run standard permission checks
        action(permissions, post)

        if post.poster and post.poster.plugin_data.get("shadow_banned"):
            raise PermissionDenied(
                pgettext(
                    "solution permission error",
                    "This post can’t be selected as the thread’s solution."
                )
            )
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CheckSelectThreadSolutionPermissionHookAction,
        permissions: "UserPermissionsProxy",
        post: Post,
    ) -> None:
        return super().__call__(action, permissions, post)


check_select_thread_solution_permission_hook = CheckSelectThreadSolutionPermissionHook()
