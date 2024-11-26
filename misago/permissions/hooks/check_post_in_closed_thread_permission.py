from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook
from ...threads.models import Thread

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class CheckPostInClosedThreadPermissionHookAction(Protocol):
    """
    A standard Misago function used to check if the user has permission to
    post in a closed thread. It raises Django's `PermissionDenied` with an
    error message if thread is closed and they can't post in it.

    # Arguments

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `thread: Thread`

    A thread to check permissions for.
    """

    def __call__(
        self,
        permissions: "UserPermissionsProxy",
        thread: Thread,
    ) -> None: ...


class CheckPostInClosedThreadPermissionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CheckPostInClosedThreadPermissionHookAction`

    A standard Misago function used to check if the user has permission to
    post in a closed thread. It raises Django's `PermissionDenied` with an
    error message if thread is closed and they can't post in it.

    See the [action](#action) section for details.

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `thread: Thread`

    A thread to check permissions for.
    """

    def __call__(
        self,
        action: CheckPostInClosedThreadPermissionHookAction,
        permissions: "UserPermissionsProxy",
        thread: Thread,
    ) -> None: ...


class CheckPostInClosedThreadPermissionHook(
    FilterHook[
        CheckPostInClosedThreadPermissionHookAction,
        CheckPostInClosedThreadPermissionHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to check if the user
    has permission to post in a closed thread. It raises Django's `PermissionDenied`
    with an error message if thread is closed and they can't post in it.

    # Example

    The code below implements a custom filter function that permits a user to
    post in the specific thread if they have a custom flag set on their account.

    ```python
    from misago.permissions.hooks import check_post_in_closed_thread_permission_hook
    from misago.permissions.proxy import UserPermissionsProxy
    from misago.threads.models import Thread

    @check_post_in_closed_thread_permission_hook.append_filter
    def check_user_can_post_in_closed_thread(
        action,
        permissions: UserPermissionsProxy,
        thread: Thread,
    ) -> None:
        user = permissions.user
        if user.is_authenticated:
            post_in_closed_categories = (
                user.plugin_data.get("post_in_closed_threads") or []
            )
        else:
            post_in_closed_categories = None

        if (
            not post_in_closed_categories
            or thread.id not in post_in_closed_categories
        ):
            action(permissions, thread)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CheckPostInClosedThreadPermissionHookAction,
        permissions: "UserPermissionsProxy",
        thread: Thread,
    ) -> None:
        return super().__call__(action, permissions, thread)


check_post_in_closed_thread_permission_hook = CheckPostInClosedThreadPermissionHook()
