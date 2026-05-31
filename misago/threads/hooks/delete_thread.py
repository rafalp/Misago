from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..models import Thread


class DeleteThreadHookAction(Protocol):
    """
    Misago function for deleting a thread.

    # Arguments

    ## `thread: Thread`

    A `Thread` to delete.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.
    """

    def __call__(
        self,
        thread: Thread,
        request: HttpRequest | None = None,
    ) -> None: ...


class DeleteThreadHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: DeleteThreadHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `thread: Thread`

    A `Thread` to delete.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    `True` if the thread was hidden, `False` otherwise.
    """

    def __call__(
        self,
        action: DeleteThreadHookAction,
        thread: Thread,
        request: HttpRequest | None = None,
    ) -> None: ...


class DeleteThreadHook(
    FilterHook[
        DeleteThreadHookAction,
        DeleteThreadHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic used to
    delete a thread.

    # Example

    Delete plugin objects related to this thread.

    ```python
    from django.http import HttpRequest
    from misago.postgres.delete import delete_all
    from misago.threads.hooks import delete_thread_hook
    from misago.threads.models import Thread
    from my_plugin.models import ThreadBoost


    @delete_thread_hook.append_filter
    def delete_thread_boosts(
        action,
        thread: Thread,
        request: HttpRequest | None = None,
    ) -> None:
        # Skip Django's delete collector logic
        delete_all(ThreadBoost, thread_id=thread.id)
        action(thread, request)
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: DeleteThreadHookAction,
        thread: Thread,
        request: HttpRequest | None = None,
    ) -> None:
        return super().__call__(action, thread, request)


delete_thread_hook = DeleteThreadHook()
