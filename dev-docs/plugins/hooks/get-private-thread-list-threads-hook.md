# `get_private_thread_list_threads_hook`

This hook wraps the standard function that Misago uses to get the complete thread data for the private thread list view.


## Location

This hook can be imported from `misago.privatethreads.hooks`:

```python
from misago.privatethreads.hooks import get_private_thread_list_threads_hook
```


## Filter

```python
def custom_get_private_thread_list_threads_filter(
    action: GetPrivateThreadListThreadsHookAction,
    request: HttpRequest,
    category: Category,
    kwargs: dict,
) -> dict:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetPrivateThreadListThreadsHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `category: Category`

The private threads category instance.


#### `kwargs: dict`

A `dict` with `kwargs` this view was called with.


### Return value

A `dict` with the template context.


## Action

```python
def get_private_thread_list_threads_action(
    request: HttpRequest, category: Category, kwargs: dict
) -> dict:
    ...
```

Misago function used to get the complete thread data for the private thread list view. Returns a `dict` that is added to the template context under the `threads` key.


### Arguments

#### `request: HttpRequest`

The request object.


#### `category: Category`

The private threads category instance.


#### `kwargs: dict`

A `dict` with `kwargs` this view was called with.


### Return value

A `dict` with the template context.


## Example

The code below implements a custom filter function makes view use a different threads list template instead of the default one.

```python
from django.http import HttpRequest
from misago.categories.models import Category
from misago.privatethreads.hooks import get_private_thread_list_threads_hook


@get_private_thread_list_threads_hook.append_filter
def replace_threads_list_template(
    action, request: HttpRequest, category: Category, kwargs: dict
) -> dict:
    data = action(request, kwargs)
    data["template_name"] = "plugin/threads_list.html"
    return data
```