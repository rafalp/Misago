from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Thread
from ...threadupdates.models import ThreadUpdate
from ..models import Poll

if TYPE_CHECKING:
    from ...users.models import User


class CloseThreadPollHookAction(Protocol):
    """
    Misago function that closes a thread's poll, updates the thread instance,
    and creates a new thread update object.

    # Arguments

    ## `thread: Thread`

    The thread to which the poll belongs.

    ## `poll: Poll`

    The poll to close.

    ## `user: User`

    The user who closed the poll, recorded as the actor of the thread update.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    A `ThreadUpdate` instance if the poll was closed, `None` if it wasn't.
    """

    def __call__(
        self,
        thread: Thread,
        poll: Poll,
        user: "User",
        request: HttpRequest | None,
    ) -> ThreadUpdate | None: ...


class CloseThreadPollHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: CloseThreadPollHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `thread: Thread`

    The thread to which the poll belongs.

    ## `poll: Poll`

    The poll to close.

    ## `user: User`

    The user who closed the poll, recorded as the actor of the thread update.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    A `ThreadUpdate` instance if the poll was closed, `None` if it wasn't.
    """

    def __call__(
        self,
        action: CloseThreadPollHookAction,
        thread: Thread,
        poll: Poll,
        user: "User",
        request: HttpRequest | None,
    ) -> ThreadUpdate | None: ...


class CloseThreadPollHook(
    FilterHook[
        CloseThreadPollHookAction,
        CloseThreadPollHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the standard logic for
    closing a thread poll.

    # Example

    This plugin automatically hides newly created thread update.

    ```python
    from django.http import HttpRequest
    from misago.polls.hooks import close_thread_poll_hook
    from misago.polls.models import Poll
    from misago.threads.models import Thread
    from misago.threadupdates.hide import hide_thread_update
    from misago.threadupdates.models import ThreadUpdate
    from misago.users.models import User

    @close_thread_poll_hook.append_filter
    def hide_closed_poll_update(
        action,
        thread: Thread,
        poll: Poll,
        user: User,
        request: HttpRequest | None,
    ) -> ThreadUpdate | None:
        thread_update = action(thread, poll, user, request)

        if thread_update:
            hide_thread_update(thread_update, request)

        return thread_update
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: CloseThreadPollHookAction,
        thread: Thread,
        poll: Poll,
        user: "User",
        request: HttpRequest | None,
    ) -> ThreadUpdate | None:
        return super().__call__(action, thread, poll, user, request)


close_thread_poll_hook = CloseThreadPollHook()
