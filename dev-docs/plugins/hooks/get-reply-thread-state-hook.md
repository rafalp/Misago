# `get_reply_thread_state_hook`

This hook wraps the standard function Misago uses to create a new `ReplyThreadState` instance for replying to a thread.


## Location

This hook can be imported from `misago.posting.hooks`:

```python
from misago.posting.hooks import get_reply_thread_state_hook
```


## Filter

```python
def custom_get_reply_thread_state_filter(
    action: GetReplyThreadStateHookAction,
    request: HttpRequest,
    thread: Thread,
    post: Post | None=None,
) -> 'ReplyThreadState':
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetReplyThreadStateHookAction`

A standard function that Misago uses to create a new `ReplyThreadState` instance for replying to a thread.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `thread: Thread`

The `Thread` instance.


#### `post: Post | None`

The `Post` instance to append posted contents to, or `None`.


### Return value

A `ReplyThreadState` instance to use to create a reply in a thread in the database.


## Action

```python
def get_reply_thread_state_action(
    request: HttpRequest, thread: Thread, post: Post | None=None
) -> 'ReplyThreadState':
    ...
```

A standard function that Misago uses to create a new `ReplyThreadState` instance for replying to a thread.


### Arguments

#### `request: HttpRequest`

The request object.


#### `thread: Thread`

The `Thread` instance.


#### `post: Post | None`

The `Post` instance to append posted contents to, or `None`.


### Return value

A `ReplyThreadState` instance to use to create a reply in a thread in the database.


## Example

The code below implements a custom filter function that stores the user's IP in the state.

```python
from django.http import HttpRequest
from misago.posting.hooks import get_reply_thread_state_hook
from misago.posting.state import ReplyThreadState
from misago.posts.models import Post
from misago.threads.models import Thread


@get_reply_thread_state_hook.append_filter
def set_poster_ip_on_reply_thread_state(
    action,
    request: HttpRequest,
    thread: Thread,
    post: Post | None = None,
) -> ReplyThreadState:
    state = action(request, thread)
    state.plugin_state["user_id"] = request.user_ip
    return state
```