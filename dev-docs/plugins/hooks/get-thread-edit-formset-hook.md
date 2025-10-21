# `get_thread_edit_formset_hook`

This hook wraps the standard function that Misago uses to create a new `ThreadEditFormset` instance with forms for editing a thread.


## Location

This hook can be imported from `misago.posting.hooks`:

```python
from misago.posting.hooks import get_thread_edit_formset_hook
```


## Filter

```python
def custom_get_thread_edit_formset_filter(
    action: GetThreadEditFormsetHookAction,
    request: HttpRequest,
    post: Post,
) -> 'ThreadEditFormset':
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetThreadEditFormsetHookAction`

The next function registered in this hook, either a custom function or Misago’s default.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `post: Post`

The `Post` instance.


### Return value

A `ThreadEditFormset` instance with forms for editing a thread.


## Action

```python
def get_thread_edit_formset_action(request: HttpRequest, post: Post) -> 'ThreadEditFormset':
    ...
```

A standard function that Misago uses to create a new `ThreadEditFormset` instance with forms for editing a thread.


### Arguments

#### `request: HttpRequest`

The request object.


#### `post: Post`

The `Post` instance.


### Return value

A `ThreadEditFormset` instance with forms for editing a thread.


## Example

The code below implements a custom filter function that adds custom form to the edit thread formset:

```python
from django.http import HttpRequest
from misago.posting.formsets import ThreadEditFormset
from misago.posting.hooks import get_thread_edit_formset_hook
from misago.threads.models import Post

from .forms import SelectUserForm


@get_thread_edit_formset_hook.append_filter
def add_select_user_form(
    action, request: HttpRequest, post: Post
) -> ThreadEditFormset:
    formset = action(request, post)

    if request.method == "POST":
        form = SelectUserForm(request.POST, prefix="select-user")
    else:
        form = SelectUserForm(prefix="select-user")

    formset.add_form(form, before="posting-post")
    return formset
```