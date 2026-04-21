from typing import TYPE_CHECKING, Protocol, Union

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...threads.models import Post, Thread

if TYPE_CHECKING:
    from ...users.models import User


class SelectThreadSolutionHookAction(Protocol):
    """
    Misago function for selecting a post as the thread’s solution.

    # Arguments

    ## `thread: Thread`

    The thread to update.

    ## `post: Post`

    The post to set as the solution.

    ## `user: User | str`

    The user who selected the solution.

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
        post: Post,
        user: Union["User", str],
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> None: ...


class SelectThreadSolutionHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: SelectThreadSolutionHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `thread: Thread`

    The thread to update.

    ## `post: Post`

    The post to set as the solution.

    ## `user: User | str`

    The user who selected the solution.

    ## `commit: bool = True`

    Whether the updated thread instance should be
    saved to the database.

    Defaults to `True`.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.
    """

    def __call__(
        self,
        action: SelectThreadSolutionHookAction,
        thread: Thread,
        post: Post,
        user: Union["User", str],
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> None: ...


class SelectThreadSolutionHook(
    FilterHook[
        SelectThreadSolutionHookAction,
        SelectThreadSolutionHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic used to
    selecting a post as the thread’s solution.

    # Example

    Record the IP address of the user who selected the solution:

    ```python
    from django.http import HttpRequest
    from misago.solutions.hooks import select_thread_solution_hook
    from misago.threads.models import Thread, Post
    from misago.users.models import User


    @select_thread_solution_hook.append_filter
    def record_solution_user_ip_address(
        action,
        thread: Thread,
        post: Post,
        user: User | str,
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> None:
        action(thread, post, user, False, request)

        if request:
            thread.plugin_data["solution_user_ip"] = request.user_ip

        if commit:
            thread.save()
    ```
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: SelectThreadSolutionHookAction,
        thread: Thread,
        post: Post,
        user: Union["User", str],
        commit: bool = True,
        request: HttpRequest | None = None,
    ) -> None:
        return super().__call__(
            action,
            thread,
            post,
            user,
            commit,
            request,
        )


select_thread_solution_hook = SelectThreadSolutionHook()
