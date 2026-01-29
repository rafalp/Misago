# `get_thread_start_state_hook`

This hook wraps the standard function Misago uses to create a new `ThreadStartState` instance for starting a new thread.


## Location

This hook can be imported from `misago.posting.hooks`:

```python
from misago.posting.hooks import get_thread_start_state_hook
```


## Filter

```python
def custom_get_thread_start_state_filter(
    action: GetThreadStartStateHookAction,
    request: HttpRequest,
    category: Category,
) -> 'ThreadStartState':
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetThreadStartStateHookAction`

The next function registered in this hook, either a custom function or Misago's default.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `category: Category`

The `Category` instance.


### Return value

A `ThreadStartState` instance to use to create a new thread in the database.


## Action

```python
def get_thread_start_state_action(request: HttpRequest, category: Category) -> 'ThreadStartState':
    ...
```

A standard function that Misago uses to create a new `ThreadStartState` instance for starting a new thread.


### Arguments

#### `request: HttpRequest`

The request object.


#### `category: Category`

The `Category` instance.


### Return value

A `ThreadStartState` instance to use to create a new thread in the database.


## Example

The code below implements a custom filter function that stores the user's IP in the state.

```python
from django.http import HttpRequest
from misago.categories.models import Category
from misago.posting.hooks import get_thread_start_state_hook
from misago.posting.state import ThreadStartState


@get_thread_start_state_hook.append_filter
def set_poster_ip_on_start_thread_state(
    action, request: HttpRequest, category: Category
) -> ThreadStartState:
    state = action(request, category)
    state.plugin_state["user_id"] = request.user_ip
    return state
```