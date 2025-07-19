from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Thread
from ...threadupdates.models import ThreadUpdate
from ..models import Poll

if TYPE_CHECKING:
    from ...users.models import User


class OpenThreadPollHookAction(Protocol):
    """
    Misago function that opens a thread's poll, updates the thread instance,
    and creates a new thread update object.

    # Arguments

    ## `thread: Thread`

    The thread to which the poll belongs.

    ## `poll: Poll`

    The poll to open.

    ## `user: User`

    The user who opened the poll, recorded as the actor of the thread update.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    A `ThreadUpdate` instance if the poll was opened, `None` if it wasn't.
    """

    def __call__(
        self,
        thread: Thread,
        poll: Poll,
        user: "User",
        request: HttpRequest | None,
    ) -> ThreadUpdate | None: ...


class OpenThreadPollHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: OpenThreadPollHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `thread: Thread`

    The thread to which the poll belongs.

    ## `poll: Poll`

    The poll to open.

    ## `user: User`

    The user who opened the poll, recorded as the actor of the thread update.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    A `ThreadUpdate` instance if the poll was opened, `None` if it wasn't.
    """

    def __call__(
        self,
        action: OpenThreadPollHookAction,
        thread: Thread,
        poll: Poll,
        user: "User",
        request: HttpRequest | None,
    ) -> ThreadUpdate | None: ...


class OpenThreadPollHook(
    FilterHook[
        OpenThreadPollHookAction,
        OpenThreadPollHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the standard logic for
    opening a opened thread poll.

    # Example

    This plugin automatically hides newly created thread update.

    ```python
    from django.http import HttpRequest
    from misago.polls.hooks import open_thread_poll_hook
    from misago.polls.models import Poll
    from misago.threads.models import Thread
    from misago.threadupdates.hide import hide_thread_update
    from misago.threadupdates.models import ThreadUpdate
    from misago.users.models import User

    @open_thread_poll_hook.append_filter
    def hide_opened_poll_update(
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
        action: OpenThreadPollHookAction,
        thread: Thread,
        poll: Poll,
        user: "User",
        request: HttpRequest | None,
    ) -> ThreadUpdate | None:
        return super().__call__(action, thread, poll, user, request)


open_thread_poll_hook = OpenThreadPollHook()
