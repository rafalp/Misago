from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..models import Poll


class DeletePollHookAction(Protocol):
    """
    Misago function for deleting a poll along with its related data.

    # Arguments

    ## `poll: Poll`

    The poll to delete.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.
    """

    def __call__(self, poll: Poll, request: HttpRequest | None) -> None: ...


class DeletePollHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: DeletePollHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `poll: Poll`

    The poll to delete.

    ## `request: HttpRequest | None`

    The request object or `None` if it was not provided.
    """

    def __call__(
        self,
        action: DeletePollHookAction,
        poll: Poll,
        request: HttpRequest | None,
    ) -> None: ...


class DeletePollHook(
    FilterHook[
        DeletePollHookAction,
        DeletePollHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the standard logic for deleting polls.

    # Example

    Delete instances of `PluginModel` related to the deleted poll:

    ```python
    from django.http import HttpRequest
    from misago.polls.hooks import delete_poll_hook
    from misago.polls.models import Poll

    from .models import PluginModel

    @delete_poll_hook.append_filter
    def delete_plugin_relations(
        action, poll: Poll, request: HttpRequest | None
    ) -> None:
        PluginModel.objects.filter(poll=poll).delete()

        # Run standard deletion logic
        action(poll, request)
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: DeletePollHookAction,
        poll: Poll,
        request: HttpRequest | None,
    ) -> None:
        return super().__call__(action, poll, request)


delete_poll_hook = DeletePollHook()
