from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..state.start import StartThreadState


class SaveStartThreadStateHookAction(Protocol):
    """
    A standard function that Misago uses to save a new thread to the database.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `state: StartThreadState`

    The `StartThreadState` object that stores all data to save to the database.
    """

    def __call__(
        self,
        request: HttpRequest,
        state: "StartThreadState",
    ): ...


class SaveStartThreadStateHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: SaveStartThreadStateHookAction`

    A standard function that Misago uses to save a new thread to the database.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `state: StartThreadState`

    The `StartThreadState` object that stores all data to save to the database.
    """

    def __call__(
        self,
        action: SaveStartThreadStateHookAction,
        request: HttpRequest,
        state: "StartThreadState",
    ): ...


class SaveStartThreadStateHook(
    FilterHook[SaveStartThreadStateHookAction, SaveStartThreadStateHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to save a new thread
    to the database.

    # Example

    The code below implements a custom filter function that stores the user's IP
    on the saved thread and post.

    ```python
    from django.http import HttpRequest
    from misago.posting.hooks import save_start_thread_state_hook
    from misago.posting.state.start import StartThreadState


    @save_start_thread_state_hook.append_filter
    def save_poster_ip_on_started_thread(
        action, request: HttpRequest, state: StartThreadState
    ):
        state.thread.plugin_data["starter_ip"] = request.user_ip
        state.post.plugin_data["poster_ip"] = request.user_ip

        action(request, state)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: SaveStartThreadStateHookAction,
        request: HttpRequest,
        state: "StartThreadState",
    ):
        return super().__call__(action, request, state)


save_start_thread_state_hook = SaveStartThreadStateHook(cache=False)
