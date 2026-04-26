from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..models import Thread


class UnlockThreadHookAction(Protocol):
    """
    Misago function for unlocking a thread.

    # Arguments

    ## `thread: Thread`

    A `Thread` to unlock.

    ## `commit: bool = True`

    Whether the updated thread instance should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    `True` if the thread was unlocked, `False` otherwise.
    """

    def __call__(
        self,
        thread: Thread,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool: ...


class UnlockThreadHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: UnlockThreadHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `thread: Thread`

    A `Thread` to unlock.

    ## `commit: bool = True`

    Whether the updated thread instance should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    `True` if the thread was unlocked, `False` otherwise.
    """

    def __call__(
        self,
        action: UnlockThreadHookAction,
        thread: Thread,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool: ...


class UnlockThreadHook(
    FilterHook[
        UnlockThreadHookAction,
        UnlockThreadHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic used to
    unlock a thread.

    # Example

    Register information about user who unlocked the thread

    ```python
    from django.http import HttpRequest
    from misago.threads.hooks import unlock_thread_hook
    from misago.threads.models import Thread


    @unlock_thread_hook.append_filter
    def register_user_that_unlocked_thread(
        action,
        thread: Thread,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool:
        if not action(thread, commit=False, request=request):
            return False

        if request:
            thread.plugin_data["unlocked_by"] = request.user.id

        if commit:
            thread.save()

        return True
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: UnlockThreadHookAction,
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


unlock_thread_hook = UnlockThreadHook()
