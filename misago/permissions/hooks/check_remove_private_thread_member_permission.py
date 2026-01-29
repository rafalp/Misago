from typing import TYPE_CHECKING, Protocol

from ...plugins.hooks import FilterHook
from ...threads.models import Thread

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class CheckRemovePrivateThreadMemberPermissionHookAction(Protocol):
    """
    Misago function that checks whether a user has permission to remove
    a private thread member. Raises `PermissionDenied` if they don't.

    # Arguments

    ## `permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `thread: Thread`

    The thread to check permissions for.

    ## `member_permissions: UserPermissionsProxy`

    A proxy object with the member's permissions.
    """

    def __call__(
        self,
        permissions: "UserPermissionsProxy",
        thread: Thread,
        member_permissions: "UserPermissionsProxy",
    ) -> None: ...


class CheckRemovePrivateThreadMemberPermissionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CheckRemovePrivateThreadMemberPermissionHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    ## `permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `thread: Thread`

    The thread to check permissions for.

    ## `member_permissions: UserPermissionsProxy`

    A proxy object with the member's permissions.
    """

    def __call__(
        self,
        action: CheckRemovePrivateThreadMemberPermissionHookAction,
        permissions: "UserPermissionsProxy",
        thread: Thread,
        member_permissions: "UserPermissionsProxy",
    ) -> None: ...


class CheckRemovePrivateThreadMemberPermissionHook(
    FilterHook[
        CheckRemovePrivateThreadMemberPermissionHookAction,
        CheckRemovePrivateThreadMemberPermissionHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic for checking whether
    a user has permission to remove a private thread member.

    # Example

    Prevent a user from removing a private thread member with a "protected" status:

    ```python
    from django.core.exceptions import PermissionDenied
    from misago.permissions.hooks import check_remove_private_thread_member_permission_hook
    from misago.permissions.proxy import UserPermissionsProxy
    from misago.threads.models import Thread

    @check_remove_private_thread_member_permission_hook.append_filter
    def check_user_can_remove_private_thread_member(
        action,
        permissions: UserPermissionsProxy,
        thread: Thread,
        member_permissions: UserPermissionsProxy,
    ) -> None:
        # Run default checks
        action(permissions, thread, member_permissions)

        if (
            not permissions.user.is_private_threads_moderator
            and member_permissions.user.plugin_data["private_threads_protect"]
        ):
            raise PermissionDenied("This member is protected. You can't remove them.")
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CheckRemovePrivateThreadMemberPermissionHookAction,
        permissions: "UserPermissionsProxy",
        thread: Thread,
        member_permissions: "UserPermissionsProxy",
    ) -> None:
        return super().__call__(action, permissions, thread, member_permissions)


check_remove_private_thread_member_permission_hook = (
    CheckRemovePrivateThreadMemberPermissionHook()
)
