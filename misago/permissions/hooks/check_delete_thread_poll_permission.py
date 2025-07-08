from typing import TYPE_CHECKING, Protocol

from ...categories.models import Category
from ...plugins.hooks import FilterHook
from ...polls.models import Poll
from ...threads.models import Thread

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class CheckDeleteThreadPollPermissionHookAction(Protocol):
    """
    Misago function used to check if the user has permission to delete
    a thread poll. Raises Django's `PermissionDenied` exception with an error
    message if the user lacks permission.

    # Arguments

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `category: Category`

    A category to check permissions for.

    ## `thread: Thread`

    A thread to check permissions for.

    ## `poll: Poll`

    A poll to check permissions for.
    """

    def __call__(
        self,
        permissions: "UserPermissionsProxy",
        category: Category,
        thread: Thread,
        poll: Poll,
    ) -> None: ...


class CheckDeleteThreadPollPermissionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CheckDeleteThreadPollPermissionHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `user_permissions: UserPermissionsProxy`

    A proxy object with the current user's permissions.

    ## `category: Category`

    A category to check permissions for.

    ## `thread: Thread`

    A thread to check permissions for.

    ## `poll: Poll`

    A poll to check permissions for.
    """

    def __call__(
        self,
        action: CheckDeleteThreadPollPermissionHookAction,
        permissions: "UserPermissionsProxy",
        category: Category,
        thread: Thread,
        poll: Poll,
    ) -> None: ...


class CheckDeleteThreadPollPermissionHook(
    FilterHook[
        CheckDeleteThreadPollPermissionHookAction,
        CheckDeleteThreadPollPermissionHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the permission check for the
    "can delete thread poll" permission.

    # Example

    Allows user to delete their own poll in a thread if it has no votes.

    ```python
    from django.core.exceptions import PermissionDenied
    from django.utils.translation import pgettext
    from misago.categories.models import Category
    from misago.polls.models import Poll
    from misago.threads.models import Thread
    from misago.permissions.checkutils import check_permissions
    from misago.permissions.hooks import check_delete_thread_poll_permission_hook
    from misago.permissions.proxy import UserPermissionsProxy

    @check_delete_thread_poll_permission_hook.append_filter
    def check_user_can_delete_poll(
        action,
        permissions: UserPermissionsProxy,
        category: Category,
        thread: Thread,
        poll: Poll,
    ) -> None:
        with check_permissions() as can_delete_poll:
            action(permissions, category, thread, poll)

        if can_delete_poll:
            return

        if (
            not permissions.user.id
            or not poll.starter_id
            or permissions.user.id != poll.starter_id
        ):
            raise PermissionDenied(
                pgettext(
                    "poll permission error",
                    "You can't delete other users polls."
                )
            )

        if poll.votes:
            raise PermissionDenied(
                pgettext(
                    "poll permission error",
                    "You can't delete polls that somebody has voted in."
                )
            )
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CheckDeleteThreadPollPermissionHookAction,
        permissions: "UserPermissionsProxy",
        category: Category,
        thread: Thread,
        poll: Poll,
    ) -> None:
        return super().__call__(action, permissions, category, thread, poll)


check_delete_thread_poll_permission_hook = CheckDeleteThreadPollPermissionHook()
