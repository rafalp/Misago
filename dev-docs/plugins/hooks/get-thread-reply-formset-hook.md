# `get_thread_reply_formset_hook`

This hook wraps the standard function that Misago uses to create a new `ThreadReplyFormset` instance with forms for posting a new thread reply.


## Location

This hook can be imported from `misago.posting.hooks`:

```python
from misago.posting.hooks import get_thread_reply_formset_hook
```


## Filter

```python
def custom_get_thread_reply_formset_filter(
    action: GetThreadReplyFormsetHookAction,
    request: HttpRequest,
    thread: Thread,
    initial: dict | None,
) -> 'ThreadReplyFormset':
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetThreadReplyFormsetHookAction`

The next function registered in this hook, either a custom function or Misago's default.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `thread: Thread`

The `Thread` instance.


#### `initial: dict | None`

A `dict` containing initial data, or `None`.


### Return value

A `ThreadReplyFormset` instance with forms for posting a new thread reply.


## Action

```python
def get_thread_reply_formset_action(
    request: HttpRequest, thread: Thread, initial: dict | None
) -> 'ThreadReplyFormset':
    ...
```

A standard function that Misago uses to create a new `ThreadReplyFormset` instance with forms for posting a new thread reply.


### Arguments

#### `request: HttpRequest`

The request object.


#### `thread: Thread`

The `Thread` instance.


#### `initial: dict | None`

A `dict` containing initial data, or `None`.


### Return value

A `ThreadReplyFormset` instance with forms for posting a new thread reply.


## Example

The code below implements a custom filter function that adds custom form to the new thread reply formset:

```python
from django.http import HttpRequest
from misago.posting.formsets import ThreadReplyFormset
from misago.posting.hooks import get_thread_reply_formset_hook
from misago.threads.models import Thread

from .forms import SelectUserForm


@get_thread_reply_formset_hook.append_filter
def add_select_user_form(
    action, request: HttpRequest, thread: Thread, initial: dict | None
) -> ThreadReplyFormset:
    formset = action(request, thread, initial)

    if request.method == "POST":
        form = SelectUserForm(request.POST, prefix="select-user")
    else:
        form = SelectUserForm(prefix="select-user")

    formset.add_form(form, before="posting-post")
    return formset
```