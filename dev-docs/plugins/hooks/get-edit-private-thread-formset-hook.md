# `get_edit_private_thread_formset_hook`

This hook wraps the standard function that Misago uses to create a new `EditPrivateThreadFormset` instance with forms for editing a private thread.


## Location

This hook can be imported from `misago.posting.hooks`:

```python
from misago.posting.hooks import get_edit_private_thread_formset_hook
```


## Filter

```python
def custom_get_edit_private_thread_formset_filter(
    action: GetEditPrivateThreadFormsetHookAction,
    request: HttpRequest,
    post: Post,
) -> 'EditPrivateThreadFormset':
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetEditPrivateThreadFormsetHookAction`

A standard function that Misago uses to create a new `EditPrivateThreadFormset` instance with forms for editing a private thread.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `post: Post`

The `Post` instance.


### Return value

A `EditPrivateThreadFormset` instance with forms for editing a private thread.


## Action

```python
def get_edit_private_thread_formset_action(request: HttpRequest, post: Post) -> 'EditPrivateThreadFormset':
    ...
```

A standard function that Misago uses to create a new `EditPrivateThreadFormset` instance with forms for editing a private thread.


### Arguments

#### `request: HttpRequest`

The request object.


#### `post: Post`

The `Post` instance.


### Return value

A `EditPrivateThreadFormset` instance with forms for editing a private thread.


## Example

The code below implements a custom filter function that adds custom form to the edit private thread formset:

```python
from django.http import HttpRequest
from misago.posting.formsets import EditPrivateThreadFormset
from misago.posting.hooks import get_edit_private_thread_formset_hook
from misago.threads.models import Post

from .forms import SelectUserForm


@get_edit_private_thread_formset_hook.append_filter
def add_select_user_form(
    action, request: HttpRequest, post: Post
) -> EditPrivateThreadFormset:
    formset = action(request, post)

    if request.method == "POST":
        form = SelectUserForm(request.POST, prefix="select-user")
    else:
        form = SelectUserForm(prefix="select-user")

    formset.add_form(form, before="posting-post")
    return formset
```