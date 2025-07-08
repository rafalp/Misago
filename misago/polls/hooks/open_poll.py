from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..models import Poll

if TYPE_CHECKING:
    from ...users.models import User


class OpenPollHookAction(Protocol):
    """
    Misago function for opening a poll.

    # Arguments

    ## `poll: Poll`

    The poll to open.

    ## `user: User`

    The user who closed the poll.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    A `bool`: `True` if the poll was opened, `False` if it wasn't
    (e.g., it was already opened).
    """

    def __call__(
        self, poll: Poll, user: "User", request: HttpRequest | None
    ) -> bool: ...


class OpenPollHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: OpenPollHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `poll: Poll`

    The poll to open.

    ## `user: User`

    The user who closed the poll.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    A `bool`: `True` if the poll was opened, `False` if it wasn't
    (e.g., it was already open).
    """

    def __call__(
        self,
        action: OpenPollHookAction,
        poll: Poll,
        user: "User",
        request: HttpRequest | None,
    ) -> bool: ...


class OpenPollHook(
    FilterHook[
        OpenPollHookAction,
        OpenPollHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the standard logic for opening polls.

    # Example

    Run extra code after poll was opened.

    ```python
    from django.http import HttpRequest
    from misago.polls.hooks import open_poll_hook
    from misago.polls.models import Poll
    from msiago.users.models import User


    @open_poll_hook.append_filter
    def open_poll(
        action, poll: Poll, user: User, request: HttpRequest | None
    ) -> bool:
        result = action(poll, user, request)
        if result:
            pass  # Run extra code here

        return result
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: OpenPollHookAction,
        poll: Poll,
        user: "User",
        request: HttpRequest | None,
    ) -> bool:
        return super().__call__(action, poll, user, request)


open_poll_hook = OpenPollHook()
