# `get_thread_breadcrumbs_hook`

This hook allows plugins to replace or extend the logic used to retrieve a thread's breadcrumbs.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import get_thread_breadcrumbs_hook
```


## Filter

```python
def custom_get_thread_breadcrumbs_filter(
    action: GetThreadBreadcrumbsHookAction,
    request: HttpRequest,
    thread: Thread,
) -> list[dict]:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetThreadBreadcrumbsHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `thread: Thread`

The `Thread` to retrieve breadcrumbs for.


### Return value

A list of `dict`s representing the thread's breadcrumbs.


## Action

```python
def get_thread_breadcrumbs_action(request: HttpRequest, thread: Thread) -> list[dict]:
    ...
```

Misago function for retrieving a thread's breadcrumbs.


### Arguments

#### `request: HttpRequest`

The request object.


#### `thread: Thread`

The `Thread` to retrieve breadcrumbs for.


### Return value

A list of `dict`s representing the thread's breadcrumbs.


## Example

Include extra data in a thread's breadcrumbs:

```python
from django.http import HttpRequest
from misago.threads.hooks import get_thread_breadcrumbs_hook
from misago.threads.models import Thread


@get_thread_breadcrumbs_hook.append_filter
def set_thread_breadcrumb_icon(
    action, request: HttpRequest, thread: Thread
) -> list[dict]:
    breadcrumbs = action(request, thread)
    if thread.is_locked:
        breadcrumbs[-1]["icon"] = "tabler/lock.svg"
    return breadcrumbs