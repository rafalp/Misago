# `get_thread_detail_view_context_data_hook`

This hook wraps the standard function that Misago uses to get the template context data for the thread detail view.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import get_thread_detail_view_context_data_hook
```


## Filter

```python
def custom_get_thread_detail_view_context_data_filter(
    action: GetThreadDetailViewContextDataHookAction,
    request: HttpRequest,
    thread: Thread,
    page: int | None,
    kwargs: dict,
) -> dict:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetThreadDetailViewContextDataHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `thread: Thread`

A `Thread` instance.


#### `page: int | None = None`

An `int` with page number or `None`.


#### `kwargs: dict`

A Python `dict` with view's keyword arguments.


### Return value

A Python `dict` with context data to use to `render` the thread detail view.


## Action

```python
def get_thread_detail_view_context_data_action(
    request: HttpRequest, thread: Thread, page: int | None, kwargs: dict
) -> dict:
    ...
```

Misago function used to get the template context data for the thread detail view.


### Arguments

#### `request: HttpRequest`

The request object.


#### `thread: Thread`

A `Thread` instance.


#### `page: int | None`

An `int` with page number or `None`.


#### `kwargs: dict`

A Python `dict` with view's keyword arguments.


### Return value

A Python `dict` with context data to use to `render` the thread detail view.


## Example

The code below implements a custom filter function that adds custom context data to the thread detail view:

```python
from django.http import HttpRequest
from misago.threads.hooks import get_thread_detail_view_context_data_hook
from misago.threads.models import Thread


@get_thread_detail_view_context_data_hook.append_filter
def include_custom_context(
    action,
    request: HttpRequest,
    thread: dict,
    page: int | None,
    kwargs: dict,
) -> dict:
    context = action(request, thread, page, kwargs)

    context["plugin_data"] = "..."

    return context
```