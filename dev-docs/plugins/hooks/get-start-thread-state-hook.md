# `get_start_thread_state_hook`

This hook wraps the standard function Misago uses to create a new `StartThreadState` instance for starting a new thread.


## Location

This hook can be imported from `misago.posting.hooks`:

```python
from misago.posting.hooks import get_start_thread_state_hook
```


## Filter

```python
def custom_get_start_thread_state_filter(
    action: GetStartThreadStateHookAction,
    request: HttpRequest,
    category: Category,
) -> 'StartThreadState':
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetStartThreadStateHookAction`

A standard function that Misago uses to create a new `StartThreadState` instance for starting a new thread.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `category: Category`

The `Category` instance.


### Return value

A `StartThreadState` instance to use to create a new thread in the database.


## Action

```python
def get_start_thread_state_action(request: HttpRequest, category: Category) -> 'StartThreadState':
    ...
```

A standard function that Misago uses to create a new `StartThreadState` instance for starting a new thread.


### Arguments

#### `request: HttpRequest`

The request object.


#### `category: Category`

The `Category` instance.


### Return value

A `StartThreadState` instance to use to create a new thread in the database.


## Example

The code below implements a custom filter function that stores the user's IP in the state.

```python
from django.http import HttpRequest
from misago.categories.models import Category
from misago.posting.hooks import get_start_thread_state_hook
from misago.posting.state import StartThreadState


@get_start_thread_state_hook.append_filter
def set_poster_ip_on_start_thread_state(
    action, request: HttpRequest, category: Category
) -> StartThreadState:
    state = action(request, category)
    state.plugin_state["user_id"] = request.user_ip
    return state
```