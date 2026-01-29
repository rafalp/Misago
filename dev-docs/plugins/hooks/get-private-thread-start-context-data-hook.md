# `get_private_thread_start_context_data_hook`

This hook wraps the function Misago uses to get the template context data for the private thread start view.


## Location

This hook can be imported from `misago.posting.hooks`:

```python
from misago.posting.hooks import get_private_thread_start_context_data_hook
```


## Filter

```python
def custom_get_private_thread_start_context_data_filter(
    action: GetPrivateThreadStartContextDataHookAction,
    request: HttpRequest,
    category: Category,
    formset: 'StartPrivateThreadFormset',
) -> dict:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetPrivateThreadStartContextDataHookAction`

The next function registered in this hook, either a custom function or Misago's default.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `category: Category`

The `Category` instance.


#### `formset: StartPrivateThreadFormset`

The `StartPrivateThreadFormset` instance.


### Return value

A Python `dict` with context data used to `render` the private thread start view.


## Action

```python
def get_private_thread_start_context_data_action(
    request: HttpRequest,
    category: Category,
    formset: 'StartPrivateThreadFormset',
) -> dict:
    ...
```

Misago function used to get the template context data for the private thread start view.


### Arguments

#### `request: HttpRequest`

The request object.


#### `category: Category`

The `Category` instance.


#### `formset: StartPrivateThreadFormset`

The `StartPrivateThreadFormset` instance.


### Return value

A Python `dict` with context data used to `render` the private thread start view.


## Example

The code below implements a custom filter function that adds extra values to the template context data:

```python
from django.http import HttpRequest
from misago.categories.models import Category
from misago.posting.formsets import StartPrivateThreadFormset
from misago.posting.hooks import get_private_thread_start_context_data_hook

@get_private_thread_start_context_data_hook.append_filter
def set_show_first_post_warning_in_context(
    action,
    request: HttpRequest,
    category: Category,
    formset: StartPrivateThreadFormset,
) -> dict:
    context = action(request, category, formset)
    context["show_first_post_warning"] = not request.user.posts
    return context
```