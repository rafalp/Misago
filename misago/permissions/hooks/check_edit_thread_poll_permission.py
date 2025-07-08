from typing import TYPE_CHECKING, Protocol

from ...categories.models import Category
from ...plugins.hooks import FilterHook
from ...polls.models import Poll
from ...threads.models import Thread

if TYPE_CHECKING:
    from ..proxy import UserPermissionsProxy


class CheckEditThreadPollPermissionHookAction(Protocol):
    """
    Misago function used to check if the user has permission to edit
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


class CheckEditThreadPollPermissionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CheckEditThreadPollPermissionHookAction`

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
        action: CheckEditThreadPollPermissionHookAction,
        permissions: "UserPermissionsProxy",
        category: Category,
        thread: Thread,
        poll: Poll,
    ) -> None: ...


class CheckEditThreadPollPermissionHook(
    FilterHook[
        CheckEditThreadPollPermissionHookAction,
        CheckEditThreadPollPermissionHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the permission check for the
    "can edit thread poll" permission.

    # Example

    Prevents a user from editing a poll in a thread if it has more than 5 votes.

    ```python
    from django.core.exceptions import PermissionDenied
    from django.utils.translation import pgettext
    from misago.categories.models import Category
    from misago.polls.models import Poll
    from misago.threads.models import Thread
    from misago.permissions.hooks import check_edit_thread_poll_permission_hook
    from misago.permissions.proxy import UserPermissionsProxy

    @check_edit_thread_poll_permission_hook.append_filter
    def check_user_can_edit_poll(
        action,
        permissions: UserPermissionsProxy,
        category: Category,
        thread: Thread,
        poll: Poll,
    ) -> None:
        # Run standard permission checks
        action(permissions, category, thread, poll)

        if poll.votes > 5:
            raise PermissionDenied(
                pgettext(
                    "poll permission error",
                    "You cannot edit polls that have received more than 5 votes."
                )
            )
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CheckEditThreadPollPermissionHookAction,
        permissions: "UserPermissionsProxy",
        category: Category,
        thread: Thread,
        poll: Poll,
    ) -> None:
        return super().__call__(action, permissions, category, thread, poll)


check_edit_thread_poll_permission_hook = CheckEditThreadPollPermissionHook()
