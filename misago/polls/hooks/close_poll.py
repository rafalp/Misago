from typing import TYPE_CHECKING, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..models import Poll

if TYPE_CHECKING:
    from ...users.models import User


class ClosePollHookAction(Protocol):
    """
    Misago function for closing a poll.

    # Arguments

    ## `poll: Poll`

    The poll to close.

    ## `user: User`

    The user who closed the poll.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    A `bool`: `True` if the poll was closed, `False` if it wasn't
    (e.g., it was already closed).
    """

    def __call__(
        self, poll: Poll, user: "User", request: HttpRequest | None
    ) -> bool: ...


class ClosePollHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: ClosePollHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `poll: Poll`

    The poll to close.

    ## `user: User`

    The user who closed the poll.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    A `bool`: `True` if the poll was closed, `False` if it wasn't
    (e.g., it was already closed).
    """

    def __call__(
        self,
        action: ClosePollHookAction,
        poll: Poll,
        user: "User",
        request: HttpRequest | None,
    ) -> bool: ...


class ClosePollHook(
    FilterHook[
        ClosePollHookAction,
        ClosePollHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the standard logic for closing polls.

    # Example

    Run extra code after poll was closed.

    ```python
    from django.http import HttpRequest
    from misago.polls.hooks import close_poll_hook
    from misago.polls.models import Poll
    from msiago.users.models import User


    @close_poll_hook.append_filter
    def close_poll(
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
        action: ClosePollHookAction,
        poll: Poll,
        user: "User",
        request: HttpRequest | None,
    ) -> bool:
        return super().__call__(action, poll, user, request)


close_poll_hook = ClosePollHook()
