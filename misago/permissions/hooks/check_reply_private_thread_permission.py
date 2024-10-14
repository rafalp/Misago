from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook
from ...threads.models import Thread

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class CheckReplyPrivateThreadPermissionHookAction(Protocol):
    """
    A standard Misago function used to check if the user has permission to
    reply to a private thread. It raises Django's `PermissionDenied` with an
    error message if they can't reply to it.

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


class CheckReplyPrivateThreadPermissionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CheckReplyPrivateThreadPermissionHookAction`

    A standard Misago function used to check if the user has permission to
    reply to a private thread. It raises Django's `PermissionDenied` with an
    error message if they can't reply to it.

    See the [action](#action) section for details.

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `thread: Thread`

    A thread to check permissions for.
    """

    def __call__(
        self,
        action: CheckReplyPrivateThreadPermissionHookAction,
        permissions: "UserPermissionsProxy",
        thread: Thread,
    ) -> None: ...


class CheckReplyPrivateThreadPermissionHook(
    FilterHook[
        CheckReplyPrivateThreadPermissionHookAction,
        CheckReplyPrivateThreadPermissionHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to check if the user
    has permission to reply to a private thread. It raises Django's `PermissionDenied`
    with an error message if they can't post in it.

    # Example

    The code below implements a custom filter function that prevents a user from
    replying to a private thread if they are a thread starter.

    ```python
    from django.core.exceptions import PermissionDenied
    from misago.permissions.hooks import check_reply_private_thread_permission_hook
    from misago.permissions.proxy import UserPermissionsProxy
    from misago.threads.models import Thread

    @check_reply_private_thread_permission_hook.append_filter
    def check_user_can_reply_in_private_thread(
        action,
        permissions: UserPermissionsProxy,
        thread: Thread,
    ) -> None:
        user = permissions.user
        if user.is_authenticated and user.id == thread.starter_id:
            raise PermissionDenied("You can't reply to threads you've started.")

        action(permissions, thread)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CheckReplyPrivateThreadPermissionHookAction,
        permissions: "UserPermissionsProxy",
        thread: Thread,
    ) -> None:
        return super().__call__(action, permissions, thread)


check_reply_private_thread_permission_hook = CheckReplyPrivateThreadPermissionHook()
