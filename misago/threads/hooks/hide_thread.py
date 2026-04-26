from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..models import Thread


class HideThreadHookAction(Protocol):
    """
    Misago function for hiding a thread.

    # Arguments

    ## `thread: Thread`

    A `Thread` to hide.

    ## `commit: bool = True`

    Whether the updated thread instance should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    `True` if the thread was hidden, `False` otherwise.
    """

    def __call__(
        self,
        thread: Thread,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool: ...


class HideThreadHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: HideThreadHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `thread: Thread`

    A `Thread` to hide.

    ## `commit: bool = True`

    Whether the updated thread instance should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    `True` if the thread was hidden, `False` otherwise.
    """

    def __call__(
        self,
        action: HideThreadHookAction,
        thread: Thread,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool: ...


class HideThreadHook(
    FilterHook[
        HideThreadHookAction,
        HideThreadHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic used to
    hide a thread.

    # Example

    Register information about user who hid the thread

    ```python
    from django.http import HttpRequest
    from misago.threads.hooks import hide_thread_hook
    from misago.threads.models import Thread


    @hide_thread_hook.append_filter
    def register_user_that_hid_thread(
        action,
        thread: Thread,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool:
        if not action(thread, commit=False, request=request):
            return False

        if request:
            thread.plugin_data["hidden_by"] = request.user.id

        if commit:
            thread.save()

        return True
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: HideThreadHookAction,
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


hide_thread_hook = HideThreadHook()
