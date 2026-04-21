from typing import Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Thread


class UnlockThreadSolutionHookAction(Protocol):
    """
    Misago function used to unlock the thread’s solution.

    # Arguments

    ## `thread: Thread`

    The thread to update.

    ## `commit: bool = True`

    Whether the updated thread instance should be
    saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.
    """

    def __call__(
        self,
        thread: Thread,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> None: ...


class UnlockThreadSolutionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: UnlockThreadSolutionHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `thread: Thread`

    The thread to update.

    ## `commit: bool = True`

    Whether the updated thread instance should be
    saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.
    """

    def __call__(
        self,
        action: UnlockThreadSolutionHookAction,
        thread: Thread,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> None: ...


class UnlockThreadSolutionHook(
    FilterHook[
        UnlockThreadSolutionHookAction,
        UnlockThreadSolutionHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic
    used to unlock the thread’s solution.

    # Example

    Record the user who unlocked the solution:

    ```python
    from django.http import HttpRequest
    from misago.solutions.hooks import unlock_thread_solution_hook
    from misago.threads.models import Thread


    @unlock_thread_solution_hook.append_filter
    def record_unlocked_solution_user(
        action,
        thread: Thread,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> None:
        action(thread, False, request)

        if request:
            thread.plugin_data.update(
                {
                    "solution_unlocked_user_id": request.user.id,
                    "solution_unlocked_user_ip": request.user_ip,
                }
            )

        if commit:
            thread.save()
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: UnlockThreadSolutionHookAction,
        thread: Thread,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> None:
        return super().__call__(
            action,
            thread,
            commit,
            request,
        )


unlock_thread_solution_hook = UnlockThreadSolutionHook()
