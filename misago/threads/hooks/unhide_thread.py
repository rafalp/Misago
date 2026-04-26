from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..models import Thread


class UnhideThreadHookAction(Protocol):
    """
    Misago function for unhiding a thread.

    # Arguments

    ## `thread: Thread`

    A `Thread` to unhide.

    ## `commit: bool = True`

    Whether the updated thread instance should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    `True` if the thread was unhidden, `False` otherwise.
    """

    def __call__(
        self,
        thread: Thread,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool: ...


class UnhideThreadHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: UnhideThreadHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `thread: Thread`

    A `Thread` to unhide.

    ## `commit: bool = True`

    Whether the updated thread instance should be saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    `True` if the thread was unhidden, `False` otherwise.
    """

    def __call__(
        self,
        action: UnhideThreadHookAction,
        thread: Thread,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool: ...


class UnhideThreadHook(
    FilterHook[
        UnhideThreadHookAction,
        UnhideThreadHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic used to
    unhide a thread.

    # Example

    Register information about user who unhidden the thread

    ```python
    from django.http import HttpRequest
    from misago.threads.hooks import unhide_thread_hook
    from misago.threads.models import Thread


    @unhide_thread_hook.append_filter
    def register_user_that_unhidden_thread(
        action,
        thread: Thread,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> bool:
        if not action(thread, commit=False, request=request):
            return False

        if request:
            thread.plugin_data["unhidden_by"] = request.user.id

        if commit:
            thread.save()

        return True
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: UnhideThreadHookAction,
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


unhide_thread_hook = UnhideThreadHook()
