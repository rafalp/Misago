# `save_edit_private_thread_post_state_hook`

This hook wraps the standard function that Misago uses to save edited private thread post to the database.


## Location

This hook can be imported from `misago.posting.hooks`:

```python
from misago.posting.hooks import save_edit_private_thread_post_state_hook
```


## Filter

```python
def custom_save_edit_private_thread_post_state_filter(
    action: SaveEditPrivateThreadPostStateHookAction,
    request: HttpRequest,
    state: 'EditPrivateThreadPostState',
):
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: SaveEditPrivateThreadPostStateHookAction`

A standard function that Misago uses to save edited private thread post to the database.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `state: EditPrivateThreadPostState`

The `EditPrivateThreadPostState` object that stores all data to save to the database.


## Action

```python
def save_edit_private_thread_post_state_action(
    request: HttpRequest, state: 'EditPrivateThreadPostState'
):
    ...
```

A standard function that Misago uses to save edited private thread post to the database.


### Arguments

#### `request: HttpRequest`

The request object.


#### `state: EditPrivateThreadPostState`

The `EditPrivateThreadPostState` object that stores all data to save to the database.


## Example

The code below implements a custom filter function that stores the user's IP on the edited post.

```python
from django.http import HttpRequest
from misago.posting.hooks import save_edit_private_thread_post_state_hook
from misago.posting.state import EditPrivateThreadPostState


@save_edit_private_thread_post_state_hook.append_filter
def save_poster_ip_on_private_thread_post(
    action, request: HttpRequest, state: EditPrivateThreadPostState
):
    state.post.plugin_data["editor_ip"] = request.user_ip

    action(request, state)
```