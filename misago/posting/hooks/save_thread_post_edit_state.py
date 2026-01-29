from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..state.edit import ThreadPostEditState


class SaveThreadPostEditStateHookAction(Protocol):
    """
    A standard function that Misago uses to save
    edited thread post to the database.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `state: ThreadPostEditState`

    The `ThreadPostEditState` object that stores all data to save to the database.
    """

    def __call__(
        self,
        request: HttpRequest,
        state: "ThreadPostEditState",
    ): ...


class SaveThreadPostEditStateHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: SaveThreadPostEditStateHookAction`

    The next function registered in this hook, either a custom function or
    Misago's default.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `state: ThreadPostEditState`

    The `ThreadPostEditState` object that stores all data to save to the database.
    """

    def __call__(
        self,
        action: SaveThreadPostEditStateHookAction,
        request: HttpRequest,
        state: "ThreadPostEditState",
    ): ...


class SaveThreadPostEditStateHook(
    FilterHook[SaveThreadPostEditStateHookAction, SaveThreadPostEditStateHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to save
    edited thread post to the database.

    # Example

    The code below implements a custom filter function that stores the user's IP
    on the edited post.

    ```python
    from django.http import HttpRequest
    from misago.posting.hooks import save_thread_post_edit_state_hook
    from misago.posting.state import ThreadPostEditState


    @save_thread_post_edit_state_hook.append_filter
    def save_poster_ip_on_thread_post(
        action, request: HttpRequest, state: ThreadPostEditState
    ):
        state.post.plugin_data["editor_ip"] = request.user_ip

        action(request, state)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: SaveThreadPostEditStateHookAction,
        request: HttpRequest,
        state: "ThreadPostEditState",
    ):
        return super().__call__(action, request, state)


save_thread_post_edit_state_hook = SaveThreadPostEditStateHook(cache=False)
