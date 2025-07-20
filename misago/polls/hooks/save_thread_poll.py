from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Thread
from ...threadupdates.models import ThreadUpdate
from ..models import Poll

if TYPE_CHECKING:
    from ...users.models import User


class SaveThreadPollHookAction(Protocol):
    """
    Misago function that saves a new poll, updates the thread instance,
    and creates a new thread update object. Used only when the poll is started
    after the thread has already been started.

    # Arguments

    ## `thread: Thread`

    The thread to update.

    ## `poll: Poll`

    The poll instance to save in the database.

    ## `user: User`

    The user who started the poll, recorded as the actor of the thread update.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    A `ThreadUpdate` instance.
    """

    def __call__(
        self,
        thread: Thread,
        poll: Poll,
        user: "User",
        request: HttpRequest | None,
    ) -> ThreadUpdate: ...


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

    The user who started the poll, recorded as the actor of the thread update.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    A `ThreadUpdate` instance.
    """

    def __call__(
        self,
        action: SaveThreadPollHookAction,
        thread: Thread,
        poll: Poll,
        user: "User",
        request: HttpRequest | None,
    ) -> ThreadUpdate: ...


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

    This plugin automatically hides newly created thread update.

    ```python
    from django.http import HttpRequest
    from misago.polls.hooks import save_thread_poll_hook
    from misago.polls.models import Poll
    from misago.threads.models import Thread
    from misago.threadupdates.hide import hide_thread_update
    from misago.threadupdates.models import ThreadUpdate
    from misago.users.models import User

    @save_thread_poll_hook.append_filter
    def hide_opened_poll_update(
        action,
        thread: Thread,
        poll: Poll,
        user: User,
        request: HttpRequest | None,
    ) -> ThreadUpdate:
        thread_update = action(thread, poll, user, request)

        if thread_update:
            hide_thread_update(thread_update, request)

        return thread_update
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
    ) -> ThreadUpdate:
        return super().__call__(action, thread, poll, user, request)


save_thread_poll_hook = SaveThreadPollHook()
