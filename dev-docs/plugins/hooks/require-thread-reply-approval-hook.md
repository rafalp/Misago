# `require_thread_reply_approval_hook`

This hook wraps the standard function Misago uses to check if a new thread reply should require moderator approval.


## Location

This hook can be imported from `misago.posting.hooks`:

```python
from misago.posting.hooks import require_thread_reply_approval_hook
```


## Filter

```python
def custom_require_thread_reply_approval_filter(
    action: RequireThreadReplyApprovalHookAction,
    state: 'ThreadReplyState',
) -> bool:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: RequireThreadReplyApprovalHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `state: ThreadReplyState`

A `ThreadReplyState` instance containing data used to create a new thread reply.


### Return value

`True` if the new thread reply should require moderator approval, or `False` otherwise.


## Action

```python
def require_thread_reply_approval_action(state: 'ThreadReplyState') -> bool:
    ...
```

A standard function that Misago uses to check if a new thread should require moderator approval.


### Arguments

#### `state: ThreadReplyState`

A `ThreadReplyState` instance containing data used to create a new thread reply.


### Return value

`True` if the new thread reply should require moderator approval, or `False` otherwise.


## Example

The code below implements a custom filter function that flags a new thread reply for moderator approval if it contains links and the user recently joined.

```python
from django.utils import timezone
from misago.posting.hooks import require_thread_reply_approval_hook
from misago.posting.state import ThreadReplyState


@require_thread_reply_approval_hook.append_filter
def require_thread_reply_approval(
    action, state: ThreadReplyState
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