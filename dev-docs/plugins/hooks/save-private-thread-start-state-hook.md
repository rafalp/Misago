# `save_private_thread_start_state_hook`

This hook wraps the standard function that Misago uses to save a new private thread to the database.


## Location

This hook can be imported from `misago.posting.hooks`:

```python
from misago.posting.hooks import save_private_thread_start_state_hook
```


## Filter

```python
def custom_save_private_thread_start_state_filter(
    action: SavePrivateThreadStartStateHookAction,
    request: HttpRequest,
    state: 'PrivateThreadStartState',
):
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: SavePrivateThreadStartStateHookAction`

The next function registered in this hook, either a custom function or Misago's default.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `state: PrivateThreadStartState`

The `PrivateThreadStartState` object that stores all data to save to the database.


## Action

```python
def save_private_thread_start_state_action(
    request: HttpRequest, state: 'PrivateThreadStartState'
):
    ...
```

A standard function that Misago uses to save a new private thread to the database.


### Arguments

#### `request: HttpRequest`

The request object.


#### `state: PrivateThreadStartState`

The `PrivateThreadStartState` object that stores all data to save to the database.


## Example

The code below implements a custom filter function that stores the user's IP on the saved thread and post.

```python
from django.http import HttpRequest
from misago.posting.hooks import save_private_thread_start_state_hook
from misago.posting.state.start import PrivateThreadStartState


@save_private_thread_start_state_hook.append_filter
def save_poster_ip_on_started_private_thread(
    action, request: HttpRequest, state: PrivateThreadStartState
):
    state.thread.plugin_data["starter_ip"] = request.user_ip
    state.post.plugin_data["poster_ip"] = request.user_ip

    action(request, state)
```