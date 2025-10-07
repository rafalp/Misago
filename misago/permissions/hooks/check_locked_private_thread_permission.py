from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook
from ...threads.models import Thread

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class CheckLockedPrivateThreadPermissionHookAction(Protocol):
    """
    Misago function that checks whether a user has permission to bypass
    a private thread's locked status. Raises `PermissionDenied` if they don't.

    # Arguments

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `thread: Thread`

    A private thread to check permissions for.
    """

    def __call__(
        self,
        permissions: "UserPermissionsProxy",
        thread: Thread,
    ) -> None: ...


class CheckLockedPrivateThreadPermissionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CheckLockedPrivateThreadPermissionHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `thread: Thread`

    A private thread to check permissions for.
    """

    def __call__(
        self,
        action: CheckLockedPrivateThreadPermissionHookAction,
        permissions: "UserPermissionsProxy",
        thread: Thread,
    ) -> None: ...


class CheckLockedPrivateThreadPermissionHook(
    FilterHook[
        CheckLockedPrivateThreadPermissionHookAction,
        CheckLockedPrivateThreadPermissionHookFilter,
    ]
):
    """
    This hook allows plugins to extend or replace the logic for checking
    whether a user has permission to bypass a private thread's locked status.

    # Example

    The code below implements a custom filter function that permits a user to
    post in the specific thread if they have a custom flag set on their account.

    ```python
    from misago.permissions.hooks import check_locked_private_thread_permission_hook
    from misago.permissions.proxy import UserPermissionsProxy
    from misago.threads.models import Thread

    @check_locked_private_thread_permission_hook.append_filter
    def check_user_can_post_in_locked_private_thread(
        action,
        permissions: UserPermissionsProxy,
        thread: Thread,
    ) -> None:
        user = permissions.user
        if user.is_authenticated:
            post_in_locked_threads = (
                user.plugin_data.get("post_in_locked_threads") or []
            )
        else:
            post_in_locked_threads = None

        if (
            not post_in_locked_threads
            or thread.id not in post_in_locked_threads
        ):
            action(permissions, thread)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CheckLockedPrivateThreadPermissionHookAction,
        permissions: "UserPermissionsProxy",
        thread: Thread,
    ) -> None:
        return super().__call__(action, permissions, thread)


check_locked_private_thread_permission_hook = CheckLockedPrivateThreadPermissionHook()
