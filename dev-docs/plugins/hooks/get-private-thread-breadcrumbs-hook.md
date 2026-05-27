# `get_private_thread_breadcrumbs_hook`

This hook allows plugins to replace or extend the logic used to retrieve a private thread's breadcrumbs.


## Location

This hook can be imported from `misago.privatethreads.hooks`:

```python
from misago.privatethreads.hooks import get_private_thread_breadcrumbs_hook
```


## Filter

```python
def custom_get_private_thread_breadcrumbs_filter(
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

A list of `dict`s representing the private thread's breadcrumbs.


## Action

```python
def get_private_thread_breadcrumbs_action(request: HttpRequest, thread: Thread) -> list[dict]:
    ...
```

Misago function for retrieving a private thread's breadcrumbs.


### Arguments

#### `request: HttpRequest`

The request object.


#### `thread: Thread`

The `Thread` to retrieve breadcrumbs for.


### Return value

A list of `dict`s representing the private thread's breadcrumbs.


## Example

Include extra data in a private thread's breadcrumbs:

```python
from django.http import HttpRequest
from misago.privatethreads.hooks import get_private_thread_breadcrumbs_hook
from misago.threads.models import Thread


@get_private_thread_breadcrumbs_hook.append_filter
def set_private_thread_breadcrumb_icon(
    action, request: HttpRequest, thread: Thread
) -> list[dict]:
    breadcrumbs = action(request, thread)
    if thread.is_locked:
        breadcrumbs[-1]["icon"] = "tabler/lock.svg"
    return breadcrumbs