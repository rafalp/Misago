# `get_edit_thread_page_context_data_hook`

This hook wraps the standard function that Misago uses to get the template context data for the edit thread page.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import get_edit_thread_page_context_data_hook
```


## Filter

```python
def custom_get_edit_thread_page_context_data_filter(
    action: GetEditThreadPostPageContextDataHookAction,
    request: HttpRequest,
    post: Post,
    formset: 'EditThreadFormset',
) -> dict:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetEditThreadPostPageContextDataHookAction`

A standard Misago function used to get the template context data for the edit thread page.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `post: Post`

The `Post` instance.


#### `formset: EditThreadFormset`

The `EditThreadFormset` instance.


### Return value

A Python `dict` with context data to use to `render` the edit thread page.


## Action

```python
def get_edit_thread_page_context_data_action(
    request: HttpRequest, post: Post, formset: 'EditThreadFormset'
) -> dict:
    ...
```

A standard Misago function used to get the template context data for the edit thread page.


### Arguments

#### `request: HttpRequest`

The request object.


#### `post: Post`

The `Post` instance.


#### `formset: EditThreadFormset`

The `EditThreadFormset` instance.


### Return value

A Python `dict` with context data to use to `render` the edit thread page.


## Example

The code below implements a custom filter function that adds extra values to the template context data:

```python
from django.http import HttpRequest
from misago.posting.formsets import EditThreadFormset
from misago.threads.hooks import get_edit_thread_page_context_data_hook
from misago.threads.models import Thread


@get_edit_thread_page_context_data_hook.append_filter
def set_show_first_post_warning_in_context(
    action,
    request: HttpRequest,
    post: Post,
    formset: EditThreadFormset,
) -> dict:
    context = action(request, thread, formset)
    context["show_first_post_warning"] = request.user.posts == 1
    return context
```