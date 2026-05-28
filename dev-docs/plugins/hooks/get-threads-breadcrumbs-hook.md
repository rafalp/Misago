# `get_threads_breadcrumbs_hook`

This hook allows plugins to replace or extend the logic used to retrieve the breadcrumbs for the threads list.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import get_threads_breadcrumbs_hook
```


## Filter

```python
def custom_get_threads_breadcrumbs_filter(
    action: GetThreadsBreadcrumbsHookAction, request: HttpRequest
) -> dict:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetThreadsBreadcrumbsHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


### Return value

A `dict` with a breadcrumbs template component.


## Action

```python
def get_threads_breadcrumbs_action(request: HttpRequest) -> dict:
    ...
```

Misago function for retrieving the breadcrumbs for the threads list.


### Arguments

#### `request: HttpRequest`

The request object.


### Return value

A `dict` with a breadcrumbs template component.


## Example

Change the icon used for the threads list breadcrumb:

```python
from django.http import HttpRequest
from misago.threads.hooks import get_threads_breadcrumbs_hook


@get_threads_breadcrumbs_hook.append_filter
def set_threads_breadcrumb_icon(
    action, request: HttpRequest
) -> dict:
    breadcrumbs = action(request, category)
    breadcrumbs["items"][-1]["icon"] = "tabler/lock.svg"
    return breadcrumbs