from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..models import Thread

if TYPE_CHECKING:
    from ...users.models import User


class GetThreadsUsersHookAction(Protocol):
    """
    A standard Misago function used to get `User` objects to display on threads list.

    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `threads: list[Thread]`

    A Python list with `Thread` instances to pull starters and last posters for.

    # Return value

    A Python `dict` with `User` instances.
    """

    def __call__(
        self, request: HttpRequest, threads: list[Thread]
    ) -> dict[int, "User"]: ...


class GetThreadsUsersHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetThreadsUsersHookAction`

    A standard Misago function used to get `User` objects to display on threads list.

    See the [action](#action) section for details.

    ## `request: HttpRequest`

    The request object.

    ## `threads: list[Thread]`

    A Python list with `Thread` instances to pull starters and last posters for.

    # Return value

    A Python `dict` with `User` instances.
    """

    def __call__(
        self,
        action: GetThreadsUsersHookAction,
        request: HttpRequest,
        threads: list[Thread],
    ) -> dict[int, "User"]: ...


class GetThreadsUsersHook(
    FilterHook[GetThreadsUsersHookAction, GetThreadsUsersHookFilter]
):
    """
    This hook wraps the standard function that Misago uses to get `User` objects
    to display on threads list.

    # Example

    The code below implements a custom filter function that excludes users with
    plugin status from the users list:

    ```python
    from django.http import HttpRequest
    from misago.threads.hooks import get_threads_users_hook


    @get_threads_users_hook.append_filter
    def include_custom_context(action, request: HttpRequest, kwargs: dict) -> dict:
        context = action(request, kwargs)

        context["plugin_data"] = "..."

        return context
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetThreadsUsersHookAction,
        request: HttpRequest,
        threads: list[Thread],
    ) -> dict[int, "User"]:
        return super().__call__(action, request, threads)


get_threads_users_hook = GetThreadsUsersHook()
