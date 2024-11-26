from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..state.start import StartPrivateThreadState


class SaveStartPrivateThreadStateHookAction(Protocol):
    """
    A standard function that Misago uses to save a new private thread to the database.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `state: StartPrivateThreadState`

    The `StartPrivateThreadState` object that stores all data to save to the database.
    """

    def __call__(
        self,
        request: HttpRequest,
        state: "StartPrivateThreadState",
    ): ...


class SaveStartPrivateThreadStateHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: SaveStartPrivateThreadStateHookAction`

    A standard function that Misago uses to save a new private thread to the database.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `state: StartPrivateThreadState`

    The `StartPrivateThreadState` object that stores all data to save to the database.
    """

    def __call__(
        self,
        action: SaveStartPrivateThreadStateHookAction,
        request: HttpRequest,
        state: "StartPrivateThreadState",
    ): ...


class SaveStartPrivateThreadStateHook(
    FilterHook[
        SaveStartPrivateThreadStateHookAction, SaveStartPrivateThreadStateHookFilter
    ]
):
    """
    This hook wraps the standard function that Misago uses to save a new private
    thread to the database.

    # Example

    The code below implements a custom filter function that stores the user's IP
    on the saved thread and post.

    ```python
    from django.http import HttpRequest
    from misago.posting.hooks import save_start_private_thread_state_hook
    from misago.posting.state.start import StartPrivateThreadState


    @save_start_private_thread_state_hook.append_filter
    def save_poster_ip_on_started_private_thread(
        action, request: HttpRequest, state: StartPrivateThreadState
    ):
        state.thread.plugin_data["starter_ip"] = request.user_ip
        state.post.plugin_data["poster_ip"] = request.user_ip

        action(request, state)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: SaveStartPrivateThreadStateHookAction,
        request: HttpRequest,
        state: "StartPrivateThreadState",
    ):
        return super().__call__(action, request, state)


save_start_private_thread_state_hook = SaveStartPrivateThreadStateHook(cache=False)
