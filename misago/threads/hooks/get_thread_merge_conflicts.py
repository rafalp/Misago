from typing import TYPE_CHECKING, Iterable, Protocol

from django.db.models import Model
from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..models import Thread

if TYPE_CHECKING:
    from ...users.models import User


class GetThreadMergeConflictsHookAction(Protocol):
    """
    Misago function for finding merge conflicts in an iterable of threads.

    # Arguments

    ## `threads: Iterable[Thread]`

    An iterable of `Thread` instances that will be merged into a single thread.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    A `dict` containing lists of models for each conflict. For example:

    ```python
    conflicts = {
        "poll": [poll_instance_1, poll_instance_2],
        "solution": [thread_1],
    }
    ```
    """

    def __call__(
        self,
        threads: Iterable[Thread],
        request: HttpRequest | None = None,
    ) -> dict[str, list[Model]]: ...


class GetThreadMergeConflictsHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: GetThreadMergeConflictsHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `threads: Iterable[Thread]`

    An iterable of `Thread` instances that will be merged into a single thread.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    A `dict` containing lists of models for each conflict.
    """

    def __call__(
        self,
        action: GetThreadMergeConflictsHookAction,
        threads: Iterable[Thread],
        request: HttpRequest | None = None,
    ) -> dict[str, list[Model]]: ...


class GetThreadMergeConflictsHook(
    FilterHook[
        GetThreadMergeConflictsHookAction,
        GetThreadMergeConflictsHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic used to
    find merge conflicts in an iterable of threads.

    # Example

    Find merge conflicts for a plugin:

    ```python
    from typing import Iterable

    from django.db.models import Model
    from django.http import HttpRequest
    from misago.threads.hooks import get_thread_merge_conflicts_hook
    from misago.threads.models import Thread
    from myplugin.models import PluginModel


    @get_thread_merge_conflicts_hook.append_filter
    def get_plugin_merge_conflicts(
        action,
        threads: Iterable[Thread],
        request: HttpRequest | None = None,
    ) -> dict[str, list[Model]]:
        conflicts = action(threads, request)

        conflicts["plugin"] = list(
            PluginModel.objects.filter(thread__in=threads).order_by("thread")
        )

        return conflicts
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: GetThreadMergeConflictsHookAction,
        threads: Iterable[Thread],
        request: HttpRequest | None = None,
    ) -> dict[str, list[Model]]:
        return super().__call__(action, threads, request)


get_thread_merge_conflicts_hook = GetThreadMergeConflictsHook()
