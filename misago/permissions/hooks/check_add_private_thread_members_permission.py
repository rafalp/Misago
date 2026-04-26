from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook
from ...threads.models import Thread

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class CheckAddPrivateThreadMembersPermissionHookAction(Protocol):
    """
    Misago function that checks whether a user has permission to add new
    members to a private thread. Raises `PermissionDenied` if they don't.

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


class CheckAddPrivateThreadMembersPermissionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CheckAddPrivateThreadMembersPermissionHookAction`

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
        action: CheckAddPrivateThreadMembersPermissionHookAction,
        permissions: "UserPermissionsProxy",
        thread: Thread,
    ) -> None: ...


class CheckAddPrivateThreadMembersPermissionHook(
    FilterHook[
        CheckAddPrivateThreadMembersPermissionHookAction,
        CheckAddPrivateThreadMembersPermissionHookFilter,
    ]
):
    """
    This hook allows plugins to extend or replace the logic for checking
    whether a user has permission to add new members to a private thread.

    # Example

    The code below implements a custom filter function that prevents user from
    adding new members to a private thread if its older than 2 hours.

    ```python
    from django.core.exceptions import PermissionDenied
    from django.utils import timezone

    from misago.permissions.hooks import check_add_private_thread_members_permission_hook
    from misago.permissions.proxy import UserPermissionsProxy
    from misago.threads.models import Thread

    @check_add_private_thread_members_permission_hook.append_filter
    def check_user_can_add_members_to_private_thread(
        action,
        permissions: UserPermissionsProxy,
        thread: Thread,
    ) -> None:
        action(permissions, thread)

        if permissions.is_private_threads_moderator:
            return

        thread_age = timezone.now() - thread.started_at
        if thread_age.total_seconds() > 7200:
            raise PermissionDenied(
                "This thread is older than 2 hours. You can't add new members to it."
            )
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CheckAddPrivateThreadMembersPermissionHookAction,
        permissions: "UserPermissionsProxy",
        thread: Thread,
    ) -> None:
        return super().__call__(action, permissions, thread)


check_add_private_thread_members_permission_hook = (
    CheckAddPrivateThreadMembersPermissionHook()
)
