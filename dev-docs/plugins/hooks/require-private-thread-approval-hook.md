# `require_private_thread_approval_hook`

This hook wraps the standard function Misago uses to check if a new private thread should require moderator approval.


## Location

This hook can be imported from `misago.posting.hooks`:

```python
from misago.posting.hooks import require_private_thread_approval_hook
```


## Filter

```python
def custom_require_private_thread_approval_filter(
    action: RequirePrivateThreadApprovalHookAction,
    state: 'PrivateThreadStartState',
) -> bool:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: RequirePrivateThreadApprovalHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `state: PrivateThreadStartState`

A `PrivateThreadStartState` instance containing data used to create a new private thread.


### Return value

`True` if the new private thread should require moderator approval, or `False` otherwise.


## Action

```python
def require_private_thread_approval_action(state: 'PrivateThreadStartState') -> bool:
    ...
```

A standard function that Misago uses to check if a new private thread should require moderator approval.


### Arguments

#### `state: PrivateThreadStartState`

A `PrivateThreadStartState` instance containing data used to create a new thread.


### Return value

`True` if the new thread should require moderator approval, or `False` otherwise.


## Example

The code below implements a custom filter function that flags a new private thread for moderator approval if the user recently joined.

```python
from django.utils import timezone
from misago.posting.hooks import require_private_thread_approval_hook
from misago.posting.state import PrivateThreadStartState


@require_private_thread_approval_hook.append_filter
def require_private_thread_approval(
    action, state: PrivateThreadStartState
) -> bool:
    if action(state):
        return True

    if state.user_permissions.bypass_content_approval:
        return False

    return (
        (timezone.now() - state.user.joined_on).total_seconds() < 72 * 3600
    )
```