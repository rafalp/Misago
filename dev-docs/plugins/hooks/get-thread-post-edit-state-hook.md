# `get_thread_post_edit_state_hook`

This hook wraps the standard function Misago uses to create a new `EditThreadPostState` instance for editing a thread post.


## Location

This hook can be imported from `misago.posting.hooks`:

```python
from misago.posting.hooks import get_thread_post_edit_state_hook
```


## Filter

```python
def custom_get_thread_post_edit_state_filter(
    action: GetEditThreadPostStateHookAction,
    request: HttpRequest,
    post: Post,
) -> 'EditThreadPostState':
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetEditThreadPostStateHookAction`

The next function registered in this hook, either a custom function or Misago's default.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `post: Post`

The `Post` instance.


### Return value

A `EditThreadPostState` instance to use to edit a post in a thread in the database.


## Action

```python
def get_thread_post_edit_state_action(request: HttpRequest, post: Post) -> 'EditThreadPostState':
    ...
```

A standard function that Misago uses to create a new `EditThreadPostState` instance for editing a thread post.


### Arguments

#### `request: HttpRequest`

The request object.


#### `post: Post`

The `Post` instance.


### Return value

A `EditThreadPostState` instance to use to edit a post in a thread in the database.


## Example

The code below implements a custom filter function that stores the user's IP in the state.

```python
from django.http import HttpRequest
from misago.posting.hooks import get_thread_post_edit_state_hook
from misago.posting.state import EditThreadPostState
from misago.threads.models import Post


@get_thread_post_edit_state_hook.append_filter
def set_poster_ip_on_edit_thread_post_state(
    action, request: HttpRequest, post: Post
) -> EditThreadPostState:
    state = action(request, post)
    state.plugin_state["user_id"] = request.user_ip
    return state
```