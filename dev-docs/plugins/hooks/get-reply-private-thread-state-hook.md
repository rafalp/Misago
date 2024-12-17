# `get_reply_private_thread_state_hook`

This hook wraps the standard function Misago uses to create a new `ReplyPrivateThreadState` instance for replying to a private thread.


## Location

This hook can be imported from `misago.posting.hooks`:

```python
from misago.posting.hooks import get_reply_private_thread_state_hook
```


## Filter

```python
def custom_get_reply_private_thread_state_filter(
    action: GetReplyPrivateThreadStateHookAction,
    request: HttpRequest,
    thread: Thread,
    post: Post | None=None,
) -> 'ReplyPrivateThreadState':
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetReplyPrivateThreadStateHookAction`

A standard function that Misago uses to create a new `ReplyPrivateThreadState` instance for replying to a private thread.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `thread: Thread`

The `Thread` instance.


#### `post: Post | None`

The `Post` instance to append posted contents to, or `None`.


### Return value

A `ReplyPrivateThreadState` instance to use to create a reply in a private thread in the database.


## Action

```python
def get_reply_private_thread_state_action(
    request: HttpRequest, thread: Thread, post: Post | None=None
) -> 'ReplyPrivateThreadState':
    ...
```

A standard function that Misago uses to create a new `ReplyPrivateThreadState` instance for replying to a private thread.


### Arguments

#### `request: HttpRequest`

The request object.


#### `thread: Thread`

The `Thread` instance.


#### `post: Post | None`

The `Post` instance to append posted contents to, or `None`.


### Return value

A `ReplyPrivateThreadState` instance to use to create a reply in a private thread in the database.


## Example

The code below implements a custom filter function that stores the user's IP in the state.

```python
from django.http import HttpRequest
from misago.posting.hooks import get_reply_private_thread_state_hook
from misago.posting.state import ReplyPrivateThreadState
from misago.threads.models import Post, Thread


@get_reply_private_thread_state_hook.append_filter
def set_poster_ip_on_reply_private_thread_state(
    action, request: HttpRequest, thread: Thread, post: Post | None = None
) -> ReplyPrivateThreadState:
    state = action(request, thread)
    state.plugin_state["user_id"] = request.user_ip
    return state
```