from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..state.edit import EditThreadPostState


class SaveEditThreadPostStateHookAction(Protocol):
    """
    A standard function that Misago uses to save
    edited thread post to the database.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `state: EditThreadPostState`

    The `EditThreadPostState` object that stores all data to save to the database.
    """

    def __call__(
        self,
        request: HttpRequest,
        state: "EditThreadPostState",
    ): ...


class SaveEditThreadPostStateHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: SaveEditThreadPostStateHookAction`

    A standard function that Misago uses to save
    edited thread post to the database.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `state: EditThreadPostState`

    The `EditThreadPostState` object that stores all data to save to the database.
    """

    def __call__(
        self,
        action: SaveEditThreadPostStateHookAction,
        request: HttpRequest,
        state: "EditThreadPostState",
    ): ...


class SaveEditThreadPostStateHook(
    FilterHook[SaveEditThreadPostStateHookAction, SaveEditThreadPostStateHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to save
    edited thread post to the database.

    # Example

    The code below implements a custom filter function that stores the user's IP
    on the edited post.

    ```python
    from django.http import HttpRequest
    from misago.posting.hooks import save_edit_thread_post_state_hook
    from misago.posting.state import EditThreadPostState


    @save_edit_thread_post_state_hook.append_filter
    def save_poster_ip_on_thread_post(
        action, request: HttpRequest, state: EditThreadPostState
    ):
        state.post.plugin_data["editor_ip"] = request.user_ip

        action(request, state)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: SaveEditThreadPostStateHookAction,
        request: HttpRequest,
        state: "EditThreadPostState",
    ):
        return super().__call__(action, request, state)


save_edit_thread_post_state_hook = SaveEditThreadPostStateHook(cache=False)
