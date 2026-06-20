from typing import Iterable, Protocol

from django.db.models import Model
from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ..models import Thread


class MergeThreadsHookAction(Protocol):
    """
    Misago function for merging threads.

    # Arguments

    ## `target: Thread`

    The `Thread` to merge `threads` into.

    ## `threads: Iterable[Thread]`

    An iterable of `Thread` instances to merge into `target`.

    These threads are deleted during the merge.

    ## `conflicts: dict[str, Model]`

    A `dict` with the conflict resolutions to use during the merge.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    The desynchronized `Thread` instance.
    """

    def __call__(
        self,
        target: Thread,
        threads: Iterable[Thread],
        conflicts: dict[str, Model],
        request: HttpRequest | None = None,
    ) -> Thread: ...


class MergeThreadsHookFilter(Protocol):
    """
    A function implemented by a plugin that can be registered in this hook.

    # Arguments

    ## `action: MergeThreadsHookAction`

    Next function registered in this hook, either a custom function or
    Misago's standard one.

    See the [action](#action) section for details.

    ## `target: Thread`

    The `Thread` to merge `threads` into.

    ## `threads: Iterable[Thread]`

    An iterable of `Thread` instances to merge into `target`.

    These threads are deleted during the merge.

    ## `conflicts: dict[str, Model]`

    A `dict` with the conflict resolutions to use during the merge.

    ## `request: HttpRequest | None`

    The request object, or `None` if not provided.

    # Return value

    The desynchronized `Thread` instance.
    """

    def __call__(
        self,
        action: MergeThreadsHookAction,
        target: Thread,
        threads: Iterable[Thread],
        conflicts: dict[str, Model],
        request: HttpRequest | None = None,
    ) -> Thread: ...


class MergeThreadsHook(
    FilterHook[
        MergeThreadsHookAction,
        MergeThreadsHookFilter,
    ]
):
    """
    This hook allows plugins to replace or extend the logic used to merge threads.

    Both the `target` thread and the categories of the merged threads must be
    synchronized after the merge to prevent data integrity errors.

    # Example

    Update `PluginModel` objects during the merge

    ```python
    from typing import Iterable

    from django.db.models import Model
    from django.http import HttpRequest
    from misago.threads.hooks import merge_threads_hook
    from misago.threads.models import Thread
    from myplugin.models import PluginModel


    @merge_threads_hook.append_filter
    def get_plugin_merge_conflicts(
        action,
        target: Thread,
        threads: Iterable[Thread],
        conflicts: dict[str, Model],
        request: HttpRequest | None = None,
    ) -> Thread:
        PluginModel.objects.filter(thread__in=threads).update(
            category=target.category, thread=target
        )

        return action(target, threads, conflicts, request)
    """

    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: MergeThreadsHookAction,
        target: Thread,
        threads: Iterable[Thread],
        conflicts: dict[str, Model],
        request: HttpRequest | None = None,
    ) -> Thread:
        return super().__call__(action, target, threads, conflicts, request)


merge_threads_hook = MergeThreadsHook()
