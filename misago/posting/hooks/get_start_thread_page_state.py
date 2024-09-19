from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...categories.models import Category
from ...plugins.hooks import FilterHook

if TYPE_CHECKING:
    from ..state.start import StartThreadState


class GetStartThreadPageStateHookAction(Protocol):
    """
    A standard function that Misago uses to create a new
    `StartThreadState` instance for the start a new thread page.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `category: Category`

    The `Category` instance.

    # Return value

    A `StartThreadState` instance to use to save new thread to the database.
    """

    def __call__(
        self,
        request: HttpRequest,
        category: Category,
    ) -> "StartThreadState": ...


class GetStartThreadPageStateHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetStartThreadPageStateHookAction`

    A standard function that Misago uses to create a new
    `StartThreadState` instance for the start a new thread page.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `category: Category`

    The `Category` instance.

    # Return value

    A `StartThreadState` instance to use to save new thread to the database.
    """

    def __call__(
        self,
        action: GetStartThreadPageStateHookAction,
        request: HttpRequest,
        category: Category,
    ) -> "StartThreadState": ...


class GetStartThreadPageStateHook(
    FilterHook[GetStartThreadPageStateHookAction, GetStartThreadPageStateHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to create a new
    `StartThreadState` instance for the start a new thread page.

    # Example

    The code below implements a custom filter function that stores the user's IP
    in the state.

    ```python
    from django.http import HttpRequest
    from misago.categories.models import Category
    from misago.posting.hooks import get_start_thread_page_state_hook
    from misago.posting.state.start import StartThreadState


    @get_start_thread_page_state_hook.append_filter
    def set_poster_ip_on_start_thread_state(
        action, request: HttpRequest, category: Category
    ) -> StartThreadState:
        state = action(request, category)
        state.plugin_state["user_id"] = request.user_ip
        return state
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetStartThreadPageStateHookAction,
        request: HttpRequest,
        category: Category,
    ) -> "StartThreadState":
        return super().__call__(action, request, category)


get_start_thread_page_state_hook = GetStartThreadPageStateHook(cache=False)
