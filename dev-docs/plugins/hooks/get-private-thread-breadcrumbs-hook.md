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
) -> dict:
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

A `dict` with a breadcrumbs template component.


## Action

```python
def get_private_thread_breadcrumbs_action(request: HttpRequest, thread: Thread) -> dict:
    ...
```

Misago function for retrieving a private thread's breadcrumbs.


### Arguments

#### `request: HttpRequest`

The request object.


#### `thread: Thread`

The `Thread` to retrieve breadcrumbs for.


### Return value

A `dict` with a breadcrumbs template component.


## Example

Change the icon used for the private thread breadcrumb:

```python
from django.http import HttpRequest
from misago.privatethreads.hooks import get_private_thread_breadcrumbs_hook
from misago.threads.models import Thread


@get_private_thread_breadcrumbs_hook.append_filter
def set_private_thread_breadcrumb_icon(
    action, request: HttpRequest, thread: Thread
) -> dict:
    breadcrumbs = action(request, thread)
    if thread.is_locked:
        breadcrumbs["items"][-1]["icon"] = "tabler/lock.svg"
    return breadcrumbs