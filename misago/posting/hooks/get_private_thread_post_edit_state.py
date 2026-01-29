from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Post

if TYPE_CHECKING:
    from ..state.edit import EditPrivateThreadPostState


class GetEditPrivateThreadPostStateHookAction(Protocol):
    """
    A standard function that Misago uses to create a new `EditPrivateThreadPostState`
    instance for editing a private thread post.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `post: Post`

    The `Post` instance.

    # Return value

    A `EditPrivateThreadPostState` instance to use to edit a post in a private thread
    in the database.
    """

    def __call__(
        self,
        request: HttpRequest,
        post: Post,
    ) -> "EditPrivateThreadPostState": ...


class GetEditPrivateThreadPostStateHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetEditPrivateThreadPostStateHookAction`

    The next function registered in this hook, either a custom function or
    Misago's default.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `post: Post`

    The `Post` instance.

    # Return value

    A `EditPrivateThreadPostState` instance to use to edit a post in a private thread
    in the database.
    """

    def __call__(
        self,
        action: GetEditPrivateThreadPostStateHookAction,
        request: HttpRequest,
        post: Post,
    ) -> "EditPrivateThreadPostState": ...


class GetEditPrivateThreadPostStateHook(
    FilterHook[
        GetEditPrivateThreadPostStateHookAction,
        GetEditPrivateThreadPostStateHookFilter,
    ]
):
    """
    This hook wraps the standard function Misago uses to create a new
    `EditPrivateThreadPostState` instance for editing a private thread post.

    # Example

    The code below implements a custom filter function that stores the user's IP
    in the state.

    ```python
    from django.http import HttpRequest
    from misago.posting.hooks import get_private_thread_post_edit_state_hook
    from misago.posting.state import EditPrivateThreadPostState
    from misago.threads.models import Post


    @get_private_thread_post_edit_state_hook.append_filter
    def set_poster_ip_on_edit_private_thread_post_state(
        action, request: HttpRequest, post: Post
    ) -> EditPrivateThreadPostState:
        state = action(request, post)
        state.plugin_state["user_id"] = request.user_ip
        return state
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetEditPrivateThreadPostStateHookAction,
        request: HttpRequest,
        post: Post,
    ) -> "EditPrivateThreadPostState":
        return super().__call__(action, request, post)


get_private_thread_post_edit_state_hook = GetEditPrivateThreadPostStateHook()
