# `get_start_private_thread_page_context_data_hook`

This hook wraps the standard function that Misago uses to get the template context data for the start private thread page.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import get_start_private_thread_page_context_data_hook
```


## Filter

```python
def custom_get_start_private_thread_page_context_data_filter(
    action: GetStartPrivateThreadPageContextDataHookAction,
    request: HttpRequest,
    category: Category,
    formset: 'StartPrivateThreadFormset',
) -> dict:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetStartPrivateThreadPageContextDataHookAction`

A standard Misago function used to get the template context data for the start private thread page.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `category: Category`

The `Category` instance.


#### `formset: StartPrivateThreadFormset`

The `StartPrivateThreadFormset` instance.


### Return value

A Python `dict` with context data to use to `render` the start private thread page.


## Action

```python
def get_start_private_thread_page_context_data_action(
    request: HttpRequest,
    category: Category,
    formset: 'StartPrivateThreadFormset',
) -> dict:
    ...
```

A standard Misago function used to get the template context data for the start private thread page.


### Arguments

#### `request: HttpRequest`

The request object.


#### `category: Category`

The `Category` instance.


#### `formset: StartPrivateThreadFormset`

The `StartPrivateThreadFormset` instance.


### Return value

A Python `dict` with context data to use to `render` the start private thread page.


## Example

The code below implements a custom filter function that adds extra values to the template context data:

```python
from django.http import HttpRequest
from misago.categories.models import Category
from misago.posting.formsets import StartPrivateThreadFormset
from misago.threads.hooks import get_start_private_thread_page_context_data_hook


@get_start_private_thread_page_context_data_hook.append_filter
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