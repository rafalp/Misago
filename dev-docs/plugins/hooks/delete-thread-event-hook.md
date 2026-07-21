# `delete_thread_event_hook`

This hook wraps a standard Misago function used to delete a `ThreadUpdate` object.


## Location

This hook can be imported from `misago.threadevents.hooks`:

```python
from misago.threadevents.hooks import delete_thread_event_hook
```


## Filter

```python
def custom_delete_thread_event_filter(
    action: DeleteThreadUpdateHookAction,
    thread_event: 'ThreadUpdate',
    request: HttpRequest | None=None,
):
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: DeleteThreadUpdateHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `thread_event: ThreadUpdate`

A `ThreadUpdate` instance to delete.


#### `request: HttpRequest | None = None`

The request object or `None` if not available.


## Action

```python
def delete_thread_event_action(
    thread_event: 'ThreadUpdate', request: HttpRequest | None=None
):
    ...
```

Misago function used to delete a `ThreadUpdate` object.


### Arguments

#### `thread_event: ThreadUpdate`

A `ThreadUpdate` instance to delete.


#### `request: HttpRequest | None = None`

The request object or `None` if not available.


## Example

The code below implements a custom filter function that logs the deletion of a thread update:

```python
import logging

from django.http import HttpRequest
from misago.threads.hooks import delete_thread_event_hook
from misago.threads.models import ThreadUpdate

logger = logging.getLogger("misago.moderation")


@delete_thread_event_hook.append_filter
def log_thread_event_deletion(
    action,
    thread_event: ThreadUpdate,
    request: HttpRequest | None = None,
) -> bool:
    logger.info(
        "Thread update was deleted",
        extra={
            "id": thread_event.id,
            "user": request.user.id if request else "",
            "ip": request.client_ip if request else "",
        },
    )
    return action(thread_event, request)
```