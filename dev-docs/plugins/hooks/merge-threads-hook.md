# `merge_threads_hook`

This hook allows plugins to replace or extend the logic used to merge threads.

Both the `target` thread and the categories of the merged threads must be synchronized after the merge to prevent data integrity errors.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import merge_threads_hook
```


## Filter

```python
def custom_merge_threads_filter(
    action: MergeThreadsHookAction,
    target: Thread,
    threads: Iterable[Thread],
    conflicts: dict[str, Model],
    commit: bool=True,
    request: HttpRequest | None=None,
) -> Thread:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: MergeThreadsHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `target: Thread`

The `Thread` to merge `threads` into.


#### `threads: Iterable[Thread]`

An iterable of `Thread` instances to merge into `target`.

These threads are deleted during the merge.


#### `conflicts: dict[str, Model]`

A `dict` with the conflict resolutions to use during the merge.


#### `commit: bool = True`

Whether the updated thread instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

The desynchronized `Thread` instance.


## Action

```python
def merge_threads_action(
    target: Thread,
    threads: Iterable[Thread],
    conflicts: dict[str, Model],
    commit: bool=True,
    request: HttpRequest | None=None,
) -> Thread:
    ...
```

Misago function for merging threads.


### Arguments

#### `target: Thread`

The `Thread` to merge `threads` into.


#### `threads: Iterable[Thread]`

An iterable of `Thread` instances to merge into `target`.

These threads are deleted during the merge.


#### `conflicts: dict[str, Model]`

A `dict` with the conflict resolutions to use during the merge.


#### `commit: bool = True`

Whether the updated thread instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

The desynchronized `Thread` instance.


## Example

Update `PluginModel` objects during the merge:

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
    commit: bool = True,
    request: HttpRequest | None = None,
) -> Thread:
    PluginModel.objects.filter(thread__in=threads).update(
        category=target.category, thread=target
    )

    return action(target, threads, conflicts, commit, request)