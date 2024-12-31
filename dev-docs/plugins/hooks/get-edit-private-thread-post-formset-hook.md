# `get_edit_private_thread_post_formset_hook`

This hook wraps the standard function that Misago uses to create a new `EditPrivateThreadPostFormset` instance with forms for editing a private thread post.


## Location

This hook can be imported from `misago.posting.hooks`:

```python
from misago.posting.hooks import get_edit_private_thread_post_formset_hook
```


## Filter

```python
def custom_get_edit_private_thread_post_formset_filter(
    action: GetEditPrivateThreadPostFormsetHookAction,
    request: HttpRequest,
    post: Post,
) -> 'EditPrivateThreadPostFormset':
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetEditPrivateThreadPostFormsetHookAction`

A standard function that Misago uses to create a new `EditPrivateThreadPostFormset` instance with forms for editing a private thread post.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `post: Post`

The `Post` instance.


### Return value

A `EditPrivateThreadPostFormset` instance with forms for editing a private thread post.


## Action

```python
def get_edit_private_thread_post_formset_action(request: HttpRequest, post: Post) -> 'EditPrivateThreadPostFormset':
    ...
```

A standard function that Misago uses to create a new `EditPrivateThreadPostFormset` instance with forms for editing a private thread post.


### Arguments

#### `request: HttpRequest`

The request object.


#### `post: Post`

The `Post` instance.


### Return value

A `EditPrivateThreadPostFormset` instance with forms for editing a private thread post.


## Example

The code below implements a custom filter function that adds custom form to the edit private thread post formset:

```python
from django.http import HttpRequest
from misago.posting.formsets import EditPrivateThreadPostFormset
from misago.posting.hooks import get_edit_private_thread_post_formset_hook
from misago.threads.models import Post

from .forms import SelectUserForm


@get_edit_private_thread_post_formset_hook.append_filter
def add_select_user_form(
    action, request: HttpRequest, post: Post
) -> EditPrivateThreadPostFormset:
    formset = action(request, post)

    if request.method == "POST":
        form = SelectUserForm(request.POST, prefix="select-user")
    else:
        form = SelectUserForm(prefix="select-user")

    formset.add_form(form, before="posting-post")
    return formset
```