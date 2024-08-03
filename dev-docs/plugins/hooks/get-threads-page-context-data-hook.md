# `get_threads_page_context_data_hook`

This hook wraps the standard function that Misago uses to get the template context data for the threads page.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import get_threads_page_context_data_hook
```


## Filter

```python
def custom_get_threads_page_context_data_filter(
    action: GetThreadsPageContextDataHookAction,
    request: HttpRequest,
    kwargs: dict,
) -> dict:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetThreadsPageContextDataHookAction`

A standard Misago function used to get the template context data for the threads page.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `kwargs: dict`

A Python `dict` with view's keyword arguments.


### Return value

A Python `dict` with context data to use to `render` the threads page.


## Action

```python
def get_threads_page_context_data_action(request: HttpRequest, kwargs: dict) -> dict:
    ...
```

A standard Misago function used to get the template context data for the threads page.


### Arguments

#### `request: HttpRequest`

The request object.


#### `kwargs: dict`

A Python `dict` with view's keyword arguments.


### Return value

A Python `dict` with context data to use to `render` the threads page.


## Example

The code below implements a custom filter function that adds custom context data to the threads page:

```python
from django.http import HttpRequest
from misago.threads.hooks import get_threads_page_context_data_hook


@get_threads_page_context_data_hook.append_filter
def include_custom_context(action, request: HttpRequest, kwargs: dict) -> dict:
    context = action(request, kwargs)

    context["plugin_data"] = "..."

    return context
```