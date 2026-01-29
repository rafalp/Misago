# `get_thread_edit_context_data_hook`

This hook wraps the function Misago uses to get the template context data for the thread edit view.


## Location

This hook can be imported from `misago.posting.hooks`:

```python
from misago.posting.hooks import get_thread_edit_context_data_hook
```


## Filter

```python
def custom_get_thread_edit_context_data_filter(
    action: GetThreadEditContextDataHookAction,
    request: HttpRequest,
    post: Post,
    formset: 'EditThreadFormset',
) -> dict:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetThreadEditContextDataHookAction`

The next function registered in this hook, either a custom function or Misago's default.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `post: Post`

The `Post` instance.


#### `formset: EditThreadFormset`

The `EditThreadFormset` instance.


### Return value

A Python `dict` with context data used to `render` the thread edit view.


## Action

```python
def get_thread_edit_context_data_action(
    request: HttpRequest, post: Post, formset: 'EditThreadFormset'
) -> dict:
    ...
```

Misago function used to get the template context data for the thread edit view.


### Arguments

#### `request: HttpRequest`

The request object.


#### `post: Post`

The `Post` instance.


#### `formset: EditThreadFormset`

The `EditThreadFormset` instance.


### Return value

A Python `dict` with context data used to `render` the thread edit view.


## Example

The code below implements a custom filter function that adds extra values to the template context data:

```python
from django.http import HttpRequest
from misago.posting.formsets import EditThreadFormset
from misago.posting.hooks import get_thread_edit_context_data_hook
from misago.threads.models import Post

@get_thread_edit_context_data_hook.append_filter
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