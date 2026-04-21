from typing import TYPE_CHECKING, Protocol, Union

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Thread

if TYPE_CHECKING:
    from ...users.models import User


class LockThreadSolutionHookAction(Protocol):
    """
    Misago function for locking the thread’s solution.

    # Arguments

    ## `thread: Thread`

    The thread to update.

    ## `user: User | str`

    The user who locked the thread's solution.

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
        user: Union["User", str],
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> None: ...


class LockThreadSolutionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: LockThreadSolutionHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `thread: Thread`

    The thread to update.

    ## `user: User | str`

    The user who locked the thread's solution.

    ## `commit: bool = True`

    Whether the updated thread instance should be
    saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.
    """

    def __call__(
        self,
        action: LockThreadSolutionHookAction,
        thread: Thread,
        user: Union["User", str],
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> None: ...


class LockThreadSolutionHook(
    FilterHook[
        LockThreadSolutionHookAction,
        LockThreadSolutionHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic used to
    lock the thread’s solution, preventing the thread’s original poster
    from changing their selection.

    # Example

    Record the IP address of the user who locked the solution:

    ```python
    from django.http import HttpRequest
    from misago.solutions.hooks import lock_thread_solution_hook
    from misago.threads.models import Thread, Post
    from misago.users.models import User


    @lock_thread_solution_hook.append_filter
    def record_solution_locked_ip_address(
        action,
        thread: Thread,
        user: User | str,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> None:
        action(thread, user, False, request)

        if request:
            thread.plugin_data["solution_locked_user_ip"] = request.user_ip

        if commit:
            thread.save()
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: LockThreadSolutionHookAction,
        thread: Thread,
        user: Union["User", str],
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> None:
        return super().__call__(
            action,
            thread,
            user,
            commit,
            request,
        )


lock_thread_solution_hook = LockThreadSolutionHook()
