# `get_private_threads_page_context_hook`

This hook wraps the standard function that Misago uses to get the template for the private threads page.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import get_private_threads_page_context_hook
```


## Filter

```python
def custom_get_private_threads_page_context_filter(
    action: GetPrivateThreadsPageContextHookAction,
    request: HttpRequest,
    kwargs: dict,
) -> dict:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetPrivateThreadsPageContextHookAction`

A standard Misago function used to get the template context for the private threads page.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `kwargs: dict`

A Python `dict` with view's keyword arguments.


### Return value

A Python `dict` with context to use to `render` the private threads page.


## Action

```python
def get_private_threads_page_context_action(request: HttpRequest, kwargs: dict) -> dict:
    ...
```

A standard Misago function used to get the template context for the private threads page.


### Arguments

#### `request: HttpRequest`

The request object.


#### `kwargs: dict`

A Python `dict` with view's keyword arguments.


### Return value

A Python `dict` with context to use to `render` the private threads page.


## Example

The code below implements a custom filter function that adds custom context to the private threads page:

```python
from django.http import HttpRequest
from misago.threads.hooks import get_private_threads_page_context_hook


@get_private_threads_page_context_hook.append_filter
def include_custom_context(action, request: HttpRequest, : dict) -> dict:
    context = action(request, kwargs)

    context["plugin_data"] = "..."

    return context
```