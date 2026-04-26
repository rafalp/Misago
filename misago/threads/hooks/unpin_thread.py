from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..models import Thread


class UnpinThreadHookAction(Protocol):
    """
    Misago function for unpinning a thread.

    # Arguments

    ## `thread: Thread`

    A `Thread` to unpin.

    ## `commit: bool = True`

    Whether the updated thread instance should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    `True` if the thread was unpinned, `False` otherwise.
    """

    def __call__(
        self,
        thread: Thread,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool: ...


class UnpinThreadHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: UnpinThreadHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `thread: Thread`

    A `Thread` to unpin.

    ## `commit: bool = True`

    Whether the updated thread instance should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    `True` if the thread was unpinned, `False` otherwise.
    """

    def __call__(
        self,
        action: UnpinThreadHookAction,
        thread: Thread,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool: ...


class UnpinThreadHook(
    FilterHook[
        UnpinThreadHookAction,
        UnpinThreadHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic used to
    unpin a thread.

    # Example

    Register user who unpinned the thread.

    ```python
    from django.http import HttpRequest
    from misago.threads.hooks import unpin_thread_hook
    from misago.threads.models import Thread


    @unpin_thread_hook.append_filter
    def register_user_that_unpinned_thread(
        action,
        thread: Thread,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool:
        if not action(thread, commit=False, request=request):
            return False

        if request:
            thread.plugin_data["unpinned_by"] = request.user.id

        if commit:
            thread.save()

        return True
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: UnpinThreadHookAction,
        thread: Thread,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool:
        return super().__call__(
            action,
            thread,
            commit,
            request,
        )


unpin_thread_hook = UnpinThreadHook()
