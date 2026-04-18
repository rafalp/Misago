# `get_context_data_hook`

This hook wraps the standard function Misago uses to check if a new thread should require moderator approval.


## Location

This hook can be imported from `misago.context_processors.hooks`:

```python
from misago.context_processors.hooks import get_context_data_hook
```


## Filter

```python
def custom_get_context_data_filter(
    action: GetContextDataHookAction, request: HttpRequest
) -> dict:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetContextDataHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `state: ThreadStartState`

A `ThreadStartState` instance containing data used to create a new thread.


### Return value

`True` if the new thread should require moderator approval, or `False` otherwise.


## Action

```python
def get_context_data_action(request: HttpRequest) -> dict:
    ...
```

A standard function that Misago uses to check if a new thread should require moderator approval.


### Arguments

#### `state: ThreadStartState`

A `ThreadStartState` instance containing data used to create a new thread.


### Return value

`True` if the new thread should require moderator approval, or `False` otherwise.


## Example

The code below implements a custom filter function that flags a new thread for moderator approval if it contains links and the user recently joined.

```python
from django.utils import timezone
from misago.posting.hooks import get_context_data_hook
from misago.posting.state import ThreadStartState


@get_context_data_hook.append_filter
def require_thread_approval(
    action, state: ThreadStartState
) -> bool:
    if action(state):
        return True

    if state.user_permissions.bypass_content_approval:
        return False

    return bool(
        (timezone.now() - state.user.joined_on).total_seconds() < 72 * 3600
        and "<a" in state.post.parsed
    )
```