# `get_private_thread_reply_state_hook`

This hook wraps the standard function Misago uses to create a new `PrivateThreadReplyState` instance for the private thread reply view.


## Location

This hook can be imported from `misago.posting.hooks`:

```python
from misago.posting.hooks import get_private_thread_reply_state_hook
```


## Filter

```python
def custom_get_private_thread_reply_state_filter(
    action: GetPrivateThreadReplyStateHookAction,
    request: HttpRequest,
    thread: Thread,
    post: Post | None=None,
) -> 'PrivateThreadReplyState':
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetPrivateThreadReplyStateHookAction`

The next function registered in this hook, either a custom function or Misago's default.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `thread: Thread`

The `Thread` instance.


#### `post: Post | None`

The `Post` instance to append posted contents to, or `None`.


### Return value

A `PrivateThreadReplyState` instance to use to create a reply in a private thread in the database.


## Action

```python
def get_private_thread_reply_state_action(
    request: HttpRequest, thread: Thread, post: Post | None=None
) -> 'PrivateThreadReplyState':
    ...
```

Misago function used to create a new `PrivateThreadReplyState` instance for the private thread reply view.


### Arguments

#### `request: HttpRequest`

The request object.


#### `thread: Thread`

The `Thread` instance.


#### `post: Post | None`

The `Post` instance to append posted contents to, or `None`.


### Return value

A `PrivateThreadReplyState` instance to use to create a reply in a private thread in the database.


## Example

The code below implements a custom filter function that stores the user's IP in the state.

```python
from django.http import HttpRequest
from misago.posting.hooks import get_private_thread_reply_state_hook
from misago.posting.state import PrivateThreadReplyState
from misago.threads.models import Post, Thread


@get_private_thread_reply_state_hook.append_filter
def set_poster_ip_on_reply_private_thread_state(
    action, request: HttpRequest, thread: Thread, post: Post | None = None
) -> PrivateThreadReplyState:
    state = action(request, thread)
    state.plugin_state["user_id"] = request.user_ip
    return state
```