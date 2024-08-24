# `get_thread_replies_page_context_data_hook`

This hook wraps the standard function that Misago uses to get the template context data for the thread replies page.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import get_thread_replies_page_context_data_hook
```


## Filter

```python
def custom_get_thread_replies_page_context_data_filter(
    action: GetThreadRepliesPageContextDataHookAction,
    request: HttpRequest,
    thread: Thread,
    page: int | None=None,
) -> dict:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetThreadRepliesPageContextDataHookAction`

A standard Misago function used to get the template context data for the thread replies page.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `thread: Thread`

A `Thread` instance.


#### `page: int | None = None`

An `int` with page number or `None`.


### Return value

A Python `dict` with context data to use to `render` the thread replies page.


## Action

```python
def get_thread_replies_page_context_data_action(
    request: HttpRequest, thread: Thread, page: int | None=None
) -> dict:
    ...
```

A standard Misago function used to get the template context data for the thread replies page.


### Arguments

#### `request: HttpRequest`

The request object.


#### `thread: Thread`

A `Thread` instance.


#### `page: int | None = None`

An `int` with page number or `None`.


### Return value

A Python `dict` with context data to use to `render` the thread replies page.


## Example

The code below implements a custom filter function that adds custom context data to the thread replies page:

```python
from django.http import HttpRequest
from misago.threads.hooks import get_thread_replies_page_context_data_hook
from misago.threads.models import Thread


@get_thread_replies_page_context_data_hook.append_filter
def include_custom_context(
    action,
    request: HttpRequest,
    thread: dict,
    page: int | None = None,
) -> dict:
    context = action(request, thread, page)

    context["plugin_data"] = "..."

    return context
```