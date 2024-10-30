from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Post

if TYPE_CHECKING:
    from ..state.edit import EditPrivateThreadReplyState


class GetEditPrivateThreadReplyStateHookAction(Protocol):
    """
    A standard function that Misago uses to create a new `EditPrivateThreadReplyState`
    instance for editing a private thread reply.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `post: Post`

    The `Post` instance.

    # Return value

    A `EditPrivateThreadReplyState` instance to use to edit a reply in a private thread
    in the database.
    """

    def __call__(
        self,
        request: HttpRequest,
        post: Post,
    ) -> "EditPrivateThreadReplyState": ...


class GetEditPrivateThreadReplyStateHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetEditPrivateThreadReplyStateHookAction`

    A standard function that Misago uses to create a new `EditPrivateThreadReplyState`
    instance for editing a private thread reply.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `post: Post`

    The `Post` instance.

    # Return value

    A `EditPrivateThreadReplyState` instance to use to edit a reply in a private thread
    in the database.
    """

    def __call__(
        self,
        action: GetEditPrivateThreadReplyStateHookAction,
        request: HttpRequest,
        post: Post,
    ) -> "EditPrivateThreadReplyState": ...


class GetEditPrivateThreadReplyStateHook(
    FilterHook[
        GetEditPrivateThreadReplyStateHookAction,
        GetEditPrivateThreadReplyStateHookFilter,
    ]
):
    """
    This hook wraps the standard function Misago uses to create a new
    `EditPrivateThreadReplyState` instance for editing a private thread reply.

    # Example

    The code below implements a custom filter function that stores the user's IP
    in the state.

    ```python
    from django.http import HttpRequest
    from misago.posting.hooks import get_edit_private_thread_reply_state_hook
    from misago.posting.state import EditPrivateThreadReplyState
    from misago.threads.models import Thread


    @get_edit_private_thread_reply_state_hook.append_filter
    def set_poster_ip_on_reply_private_thread_state(
        action, request: HttpRequest, post: Post
    ) -> EditPrivateThreadReplyState:
        state = action(request, post)
        state.plugin_state["user_id"] = request.user_ip
        return state
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetEditPrivateThreadReplyStateHookAction,
        request: HttpRequest,
        post: Post,
    ) -> "EditPrivateThreadReplyState":
        return super().__call__(action, request, post)


get_edit_private_thread_reply_state_hook = GetEditPrivateThreadReplyStateHook()
