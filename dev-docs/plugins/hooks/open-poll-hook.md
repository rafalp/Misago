# `open_poll_hook`

This hook allows plugins to replace or extend the standard logic for opening polls.


## Location

This hook can be imported from `misago.polls.hooks`:

```python
from misago.polls.hooks import open_poll_hook
```


## Filter

```python
def custom_open_poll_filter(
    action: OpenPollHookAction,
    poll: Poll,
    user: 'User',
    request: HttpRequest | None,
) -> bool:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: OpenPollHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `poll: Poll`

The poll to open.


#### `user: User`

The user who closed the poll.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

A `bool`: `True` if the poll was opened, `False` if it wasn't (e.g., it was already open).


## Action

```python
def open_poll_action(
    poll: Poll, user: 'User', request: HttpRequest | None
) -> bool:
    ...
```

Misago function for opening a poll.


### Arguments

#### `poll: Poll`

The poll to open.


#### `user: User`

The user who closed the poll.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


### Return value

A `bool`: `True` if the poll was opened, `False` if it wasn't (e.g., it was already opened).


## Example

Run extra code after poll was opened.

```python
from django.http import HttpRequest
from misago.polls.hooks import open_poll_hook
from misago.polls.models import Poll
from msiago.users.models import User


@open_poll_hook.append_filter
def open_poll(
    action, poll: Poll, user: User, request: HttpRequest | None
) -> bool:
    result = action(poll, user, request)
    if result:
        pass  # Run extra code here

    return result
```