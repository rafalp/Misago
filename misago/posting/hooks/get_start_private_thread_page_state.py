from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...categories.models import Category
from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..state.start import StartPrivateThreadState


class GetStartPrivateThreadPageStateHookAction(Protocol):
    """
    A standard function that Misago uses to create a new
    `StartPrivateThreadState` instance for the start a new private thread page.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `category: Category`

    The `Category` instance.

    # Return value

    A `StartPrivateThreadState` instance to use to save new private thread
    to the database.
    """

    def __call__(
        self,
        request: HttpRequest,
        category: Category,
    ) -> "StartPrivateThreadState": ...


class GetStartPrivateThreadPageStateHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetStartPrivateThreadPageStateHookAction`

    A standard function that Misago uses to create a new
    `StartPrivateThreadState` instance for the start a new private thread page.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `category: Category`

    The `Category` instance.

    # Return value

    A `StartPrivateThreadState` instance to use to save new private thread
    to the database.
    """

    def __call__(
        self,
        action: GetStartPrivateThreadPageStateHookAction,
        request: HttpRequest,
        category: Category,
    ) -> "StartPrivateThreadState": ...


class GetStartPrivateThreadPageStateHook(
    FilterHook[
        GetStartPrivateThreadPageStateHookAction,
        GetStartPrivateThreadPageStateHookFilter,
    ]
):
    """
    This hook wraps the standard function that Misago uses to create a new
    `StartPrivateThreadState` instance for the start a new private thread page.
    # Example

    The code below implements a custom filter function that stores the user's IP
    in the state.

    ```python
    from django.http import HttpRequest
    from misago.categories.models import Category
    from misago.posting.hooks import get_start_private_thread_page_state_hook
    from misago.posting.state.start import StartPrivateThreadState


    @get_start_private_thread_page_state_hook.append_filter
    def set_poster_ip_on_start_private_thread_page_state(
        action, request: HttpRequest, category: Category
    ) -> StartPrivateThreadState:
        state = action(request, category)
        state.plugin_state["user_id"] = request.user_ip
        return state
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetStartPrivateThreadPageStateHookAction,
        request: HttpRequest,
        category: Category,
    ) -> "StartPrivateThreadState":
        return super().__call__(action, request, category)


get_start_private_thread_page_state_hook = GetStartPrivateThreadPageStateHook(
    cache=False
)
