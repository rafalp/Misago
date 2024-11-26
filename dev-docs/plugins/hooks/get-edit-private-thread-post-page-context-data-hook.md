# `get_edit_private_thread_post_page_context_data_hook`

This hook wraps the standard function that Misago uses to get the template context data for the edit private thread post page.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import get_edit_private_thread_post_page_context_data_hook
```


## Filter

```python
def custom_get_edit_private_thread_post_page_context_data_filter(
    action: GetEditPrivateThreadPostPageContextDataHookAction,
    request: HttpRequest,
    post: Post,
    formset: 'EditPrivateThreadPostFormset',
) -> dict:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetEditPrivateThreadPostPageContextDataHookAction`

A standard Misago function used to get the template context data for the edit private thread post page.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `post: Post`

The `Post` instance.


#### `formset: EditPrivateThreadPostFormset`

The `EditPrivateThreadPostFormset` instance.


### Return value

A Python `dict` with context data to use to `render` the edit private thread post page.


## Action

```python
def get_edit_private_thread_post_page_context_data_action(
    request: HttpRequest,
    post: Post,
    formset: 'EditPrivateThreadPostFormset',
) -> dict:
    ...
```

A standard Misago function used to get the template context data for the edit private thread post page.


### Arguments

#### `request: HttpRequest`

The request object.


#### `post: Post`

The `Post` instance.


#### `formset: EditPrivateThreadPostFormset`

The `EditPrivateThreadPostFormset` instance.


### Return value

A Python `dict` with context data to use to `render` the edit private thread post page.


## Example

The code below implements a custom filter function that adds extra values to the template context data:

```python
from django.http import HttpRequest
from misago.posting.formsets import EditPrivateThreadPostFormset
from misago.threads.hooks import get_edit_private_thread_post_page_context_data_hook
from misago.threads.models import Thread


@get_edit_private_thread_post_page_context_data_hook.append_filter
def set_show_first_post_warning_in_context(
    action,
    request: HttpRequest,
    post: Post,
    formset: EditPrivateThreadPostFormset,
) -> dict:
    context = action(request, thread, formset)
    context["show_first_post_warning"] = request.user.posts == 1
    return context
```