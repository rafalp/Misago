# `save_private_thread_post_edit_state_hook`

This hook wraps the standard function that Misago uses to save edited private thread post to the database.


## Location

This hook can be imported from `misago.posting.hooks`:

```python
from misago.posting.hooks import save_private_thread_post_edit_state_hook
```


## Filter

```python
def custom_save_private_thread_post_edit_state_filter(
    action: SavePrivateThreadPostEditStateHookAction,
    request: HttpRequest,
    state: 'PrivateThreadPostEditState',
):
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: SavePrivateThreadPostEditStateHookAction`

The next function registered in this hook, either a custom function or Misago's default.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `state: PrivateThreadPostEditState`

The `PrivateThreadPostEditState` object that stores all data to save to the database.


## Action

```python
def save_private_thread_post_edit_state_action(
    request: HttpRequest, state: 'PrivateThreadPostEditState'
):
    ...
```

A standard function that Misago uses to save edited private thread post to the database.


### Arguments

#### `request: HttpRequest`

The request object.


#### `state: PrivateThreadPostEditState`

The `PrivateThreadPostEditState` object that stores all data to save to the database.


## Example

The code below implements a custom filter function that stores the user's IP on the edited post.

```python
from django.http import HttpRequest
from misago.posting.hooks import save_private_thread_post_edit_state_hook
from misago.posting.state import PrivateThreadPostEditState


@save_private_thread_post_edit_state_hook.append_filter
def save_poster_ip_on_private_thread_post(
    action, request: HttpRequest, state: PrivateThreadPostEditState
):
    state.post.plugin_data["editor_ip"] = request.user_ip

    action(request, state)
```