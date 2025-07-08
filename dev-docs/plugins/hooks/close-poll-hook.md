# `close_poll_hook`

This hook allows plugins to replace or extend the standard logic for closing polls.


## Location

This hook can be imported from `misago.polls.hooks`:

```python
from misago.polls.hooks import close_poll_hook
```


## Filter

```python
def custom_close_poll_filter(
    action: ClosePollHookAction,
    poll: Poll,
    user: 'User',
    request: HttpRequest | None,
) -> bool:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: ClosePollHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `poll: Poll`

The poll to close.


#### `user: User`

The user who closed the poll.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

A `bool`: `True` if the poll was closed, `False` if it wasn't (e.g., it was already closed).


## Action

```python
def close_poll_action(
    poll: Poll, user: 'User', request: HttpRequest | None
) -> bool:
    ...
```

Misago function for closing a poll.


### Arguments

#### `poll: Poll`

The poll to close.


#### `user: User`

The user who closed the poll.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

A `bool`: `True` if the poll was closed, `False` if it wasn't (e.g., it was already closed).


## Example

Run extra code after poll was closed.

```python
from django.http import HttpRequest
from misago.polls.hooks import close_poll_hook
from misago.polls.models import Poll
from msiago.users.models import User


@close_poll_hook.append_filter
def close_poll(
    action, poll: Poll, user: User, request: HttpRequest | None
) -> bool:
    result = action(poll, user, request)
    if result:
        pass  # Run extra code here

    return result
```