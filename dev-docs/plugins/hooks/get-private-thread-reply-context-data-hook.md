# `get_private_thread_reply_context_data_hook`

This hook wraps the function Misago uses to get the template context data for the private thread reply view.


## Location

This hook can be imported from `misago.posting.hooks`:

```python
from misago.posting.hooks import get_private_thread_reply_context_data_hook
```


## Filter

```python
def custom_get_private_thread_reply_context_data_filter(
    action: GetPrivateThreadReplyContextDataHookAction,
    request: HttpRequest,
    thread: Thread,
    formset: 'ReplyPrivateThreadFormset',
) -> dict:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetPrivateThreadReplyContextDataHookAction`

The next function registered in this hook, either a custom function or Misago's default.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `thread: Thread`

The `Thread` instance.


#### `formset: ReplyPrivateThreadFormset`

The `ReplyPrivateThreadFormset` instance.


### Return value

A Python `dict` with context data used to `render` the private thread thread reply view.


## Action

```python
def get_private_thread_reply_context_data_action(
    request: HttpRequest,
    thread: Thread,
    formset: 'ReplyPrivateThreadFormset',
) -> dict:
    ...
```

Misago function used to get the template context data for the private thread reply view.


### Arguments

#### `request: HttpRequest`

The request object.


#### `thread: Thread`

The `Thread` instance.


#### `formset: ReplyPrivateThreadFormset`

The `ReplyPrivateThreadFormset` instance.


### Return value

A Python `dict` with context data used to `render` the private thread thread reply view.


## Example

The code below implements a custom filter function that adds extra values to the template context data:

```python
from django.http import HttpRequest
from misago.posting.formsets import ReplyPrivateThreadFormset
from misago.posting.hooks import get_private_thread_reply_context_data_hook
from misago.threads.models import Thread


@get_private_thread_reply_context_data_hook.append_filter
def set_show_first_post_warning_in_context(
    action,
    request: HttpRequest,
    thread: Thread,
    formset: ReplyPrivateThreadFormset,
) -> dict:
    context = action(request, thread, formset)
    context["show_first_post_warning"] = not request.user.posts
    return context
```