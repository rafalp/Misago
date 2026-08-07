from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threadevents.models import ThreadEvent
from ...threads.models import Thread
from ..models import Poll

if TYPE_CHECKING:
    from ...users.models import User


class SaveThreadPollHookAction(Protocol):
    """
    Misago function that saves a new poll, updates the thread instance,
    and creates a new thread event object. Used only when the poll is started
    after the thread has already been started.

    # Arguments

    ## `thread: Thread`

    The thread to update.

    ## `poll: Poll`

    The poll instance to save in the database.

    ## `user: User`

    The user who started the poll, recorded as the actor of the thread event.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    A `ThreadEvent` instance.
    """

    def __call__(
        self,
        thread: Thread,
        poll: Poll,
        user: "User",
        request: HttpRequest | None,
    ) -> ThreadEvent: ...


class SaveThreadPollHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: SaveThreadPollHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `thread: Thread`

    The thread to update.

    ## `poll: Poll`

    The poll instance to save in the database.

    ## `user: User`

    The user who started the poll, recorded as the actor of the thread event.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    A `ThreadEvent` instance.
    """

    def __call__(
        self,
        action: SaveThreadPollHookAction,
        thread: Thread,
        poll: Poll,
        user: "User",
        request: HttpRequest | None,
    ) -> ThreadEvent: ...


class SaveThreadPollHook(
    FilterHook[
        SaveThreadPollHookAction,
        SaveThreadPollHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the standard logic for
    saving a new poll in a thread.

    # Example

    This plugin automatically hides newly created thread event.

    ```python
    from django.http import HttpRequest
    from misago.polls.hooks import save_thread_poll_hook
    from misago.polls.models import Poll
    from misago.threads.models import Thread
    from misago.threadevents.hide import hide_thread_event
    from misago.threadevents.models import ThreadEvent
    from misago.users.models import User

    @save_thread_poll_hook.append_filter
    def hide_opened_poll_event(
        action,
        thread: Thread,
        poll: Poll,
        user: User,
        request: HttpRequest | None,
    ) -> ThreadEvent:
        thread_event = action(thread, poll, user, request)

        if thread_event:
            hide_thread_event(thread_event, request)

        return thread_event
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: SaveThreadPollHookAction,
        thread: Thread,
        poll: Poll,
        user: "User",
        request: HttpRequest | None,
    ) -> ThreadEvent:
        return super().__call__(action, thread, poll, user, request)


save_thread_poll_hook = SaveThreadPollHook()
