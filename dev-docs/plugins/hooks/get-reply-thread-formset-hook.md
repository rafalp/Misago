# `get_reply_thread_formset_hook`

This hook wraps the standard function that Misago uses to create a new `ReplyThreadFormset` instance with forms for posting a new thread reply.


## Location

This hook can be imported from `misago.posting.hooks`:

```python
from misago.posting.hooks import get_reply_thread_formset_hook
```


## Filter

```python
def custom_get_reply_thread_formset_filter(
    action: GetReplyThreadFormsetHookAction,
    request: HttpRequest,
    thread: Thread,
) -> 'ReplyThreadFormset':
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetReplyThreadFormsetHookAction`

The next function registered in this hook, either a custom function or Misago’s default.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `thread: Thread`

The `Thread` instance.


### Return value

A `ReplyThreadFormset` instance with forms for posting a new thread reply.


## Action

```python
def get_reply_thread_formset_action(request: HttpRequest, thread: Thread) -> 'ReplyThreadFormset':
    ...
```

A standard function that Misago uses to create a new `ReplyThreadFormset` instance with forms for posting a new thread reply.


### Arguments

#### `request: HttpRequest`

The request object.


#### `thread: Thread`

The `Thread` instance.


### Return value

A `ReplyThreadFormset` instance with forms for posting a new thread reply.


## Example

The code below implements a custom filter function that adds custom form to the new thread reply formset:

```python
from django.http import HttpRequest
from misago.posting.formsets import ReplyThreadFormset
from misago.posting.hooks import get_reply_thread_formset_hook
from misago.threads.models import Thread

from .forms import SelectUserForm


@get_reply_thread_formset_hook.append_filter
def add_select_user_form(
    action, request: HttpRequest, thread: Thread
) -> ReplyThreadFormset:
    formset = action(request, thread)

    if request.method == "POST":
        form = SelectUserForm(request.POST, prefix="select-user")
    else:
        form = SelectUserForm(prefix="select-user")

    formset.add_form(form, before="posting-post")
    return formset
```