# `get_thread_merge_conflicts_hook`

This hook allows plugins to replace or extend the logic used to find merge conflicts in an iterable of threads.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import get_thread_merge_conflicts_hook
```


## Filter

```python
def custom_get_thread_merge_conflicts_filter(
    action: GetThreadMergeConflictsHookAction,
    threads: Iterable[Thread],
    request: HttpRequest | None=None,
) -> dict[str, list[Model]]:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetThreadMergeConflictsHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `threads: Iterable[Thread]`

An iterable of `Thread` instances that will be merged into a single thread.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

A `dict` containing lists of models for each conflict.


## Action

```python
def get_thread_merge_conflicts_action(
    threads: Iterable[Thread], request: HttpRequest | None=None
) -> dict[str, list[Model]]:
    ...
```

Misago function for finding merge conflicts in an iterable of threads.


### Arguments

#### `threads: Iterable[Thread]`

An iterable of `Thread` instances that will be merged into a single thread.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

A `dict` containing lists of models for each conflict. For example:

```python
conflicts = {
    "poll": [poll_instance_1, poll_instance_2],
    "solution": [thread_1],
}
```


## Example

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