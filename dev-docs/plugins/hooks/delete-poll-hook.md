# `delete_poll_hook`

This hook allows plugins to replace or extend the standard logic for deleting polls.


## Location

This hook can be imported from `misago.polls.hooks`:

```python
from misago.polls.hooks import delete_poll_hook
```


## Filter

```python
def custom_delete_poll_filter(
    action: DeletePollHookAction, poll: Poll, request: HttpRequest | None
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: DeletePollHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `poll: Poll`

The poll to delete.


#### `request: HttpRequest | None`

The request object or `None` if it was not provided.


## Action

```python
def delete_poll_action(poll: Poll, request: HttpRequest | None) -> None:
    ...
```

Misago function for deleting a poll along with its related data.


### Arguments

#### `poll: Poll`

The poll to delete.


#### `request: HttpRequest | None`

The request object, or `None` if not provided.


## Example

Delete instances of `PluginModel` related to the deleted poll:

```python
from django.http import HttpRequest
from misago.polls.hooks import delete_poll_hook
from misago.polls.models import Poll

from .models import PluginModel

@delete_poll_hook.append_filter
def delete_plugin_relations(
    action, poll: Poll, request: HttpRequest | None
) -> None:
    PluginModel.objects.filter(poll=poll).delete()

    # Run standard deletion logic
    action(poll, request)
```