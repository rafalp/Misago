from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Thread
from ..models import Poll

if TYPE_CHECKING:
    from ...users.models import User


class EditThreadPollHookAction(Protocol):
    """
    Misago function that saves an edited poll.

    # Arguments

    ## `thread: Thread`

    The thread instance.

    ## `poll: Poll`

    The poll instance to save in the database.

    ## `user: User`

    The user who edited the poll.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.
    """

    def __call__(
        self,
        thread: Thread,
        poll: Poll,
        user: "User",
        request: HttpRequest | None,
    ) -> None: ...


class EditThreadPollHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: EditThreadPollHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `thread: Thread`

    The thread instance.

    ## `poll: Poll`

    The poll instance to save in the database.

    ## `user: User`

    The user who edited the poll.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.
    """

    def __call__(
        self,
        action: EditThreadPollHookAction,
        thread: Thread,
        poll: Poll,
        user: "User",
        request: HttpRequest | None,
    ) -> None: ...


class EditThreadPollHook(
    FilterHook[
        EditThreadPollHookAction,
        EditThreadPollHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the standard logic for
    saving an edited poll in the database.

    # Example

    This plugin saves the user who edited the poll in its `plugin_data` field.

    ```python
    from django.http import HttpRequest
    from django.utils import timezone
    from misago.polls.hooks import edit_thread_poll_hook
    from misago.polls.models import Poll
    from misago.threads.models import Thread
    from misago.users.models import User

    @edit_thread_poll_hook.append_filter
    def save_poll_edit_data(
        action,
        thread: Thread,
        poll: Poll,
        user: User,
        request: HttpRequest | None,
    ) -> None:
        poll.plugin_data.set_default("edits", []).append(
            {
                "user_id": user.id,
                "username": user.username,
                "datetime": timezone.now().isoformat(),
            }
        )

        action(thread, poll, user, request)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: EditThreadPollHookAction,
        thread: Thread,
        poll: Poll,
        user: "User",
        request: HttpRequest | None,
    ) -> None:
        return super().__call__(action, thread, poll, user, request)


edit_thread_poll_hook = EditThreadPollHook()
