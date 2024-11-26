# `get_start_thread_page_context_data_hook`

This hook wraps the standard function that Misago uses to get the template context data for the start thread page.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import get_start_thread_page_context_data_hook
```


## Filter

```python
def custom_get_start_thread_page_context_data_filter(
    action: GetStartThreadPageContextDataHookAction,
    request: HttpRequest,
    category: Category,
    formset: 'StartThreadFormset',
) -> dict:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetStartThreadPageContextDataHookAction`

A standard Misago function used to get the template context data for the start thread page.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `category: Category`

The `Category` instance.


#### `formset: StartThreadFormset`

The `StartThreadFormset` instance.


### Return value

A Python `dict` with context data to use to `render` the start thread page.


## Action

```python
def get_start_thread_page_context_data_action(
    request: HttpRequest,
    category: Category,
    formset: 'StartThreadFormset',
) -> dict:
    ...
```

A standard Misago function used to get the template context data for the start thread page.


### Arguments

#### `request: HttpRequest`

The request object.


#### `category: Category`

The `Category` instance.


#### `formset: StartThreadFormset`

The `StartThreadFormset` instance.


### Return value

A Python `dict` with context data to use to `render` the start thread page.


## Example

The code below implements a custom filter function that adds extra values to the template context data:

```python
from django.http import HttpRequest
from misago.categories.models import Category
from misago.posting.formsets import StartThreadFormset
from misago.threads.hooks import get_start_thread_page_context_data_hook


@get_start_thread_page_context_data_hook.append_filter
def set_show_first_post_warning_in_context(
    action,
    request: HttpRequest,
    category: Category,
    formset: StartThreadFormset,
) -> dict:
    context = action(request, category, formset)
    context["show_first_post_warning"] = not request.user.posts
    return context
```