# `delete_thread_update_hook`

This hook wraps a standard Misago function used to delete a `ThreadUpdate` object.


## Location

This hook can be imported from `misago.threadupdates.hooks`:

```python
from misago.threadupdates.hooks import delete_thread_update_hook
```


## Filter

```python
def custom_delete_thread_update_filter(
    action: DeleteThreadUpdateHookAction,
    thread_update: 'ThreadUpdate',
    request: HttpRequest | None=None,
):
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: DeleteThreadUpdateHookAction`

Misago function used to delete a `ThreadUpdate` object.


#### `thread_update: ThreadUpdate`

A `ThreadUpdate` instance to delete.


#### `request: HttpRequest | None = None`

The request object or `None` if not available.


## Action

```python
def delete_thread_update_action(
    thread_update: 'ThreadUpdate', request: HttpRequest | None=None
):
    ...
```

Misago function used to delete a `ThreadUpdate` object.


### Arguments

#### `thread_update: ThreadUpdate`

A `ThreadUpdate` instance to delete.


#### `request: HttpRequest | None = None`

The request object or `None` if not available.


## Example

The code below implements a custom filter function that logs the deletion of a thread update:

```python
import logging

from django.http import HttpRequest
from misago.threads.hooks import delete_thread_update_hook
from misago.threads.models import ThreadUpdate

logger = logging.getLogger("misago.moderation")


@delete_thread_update_hook.append_filter
def log_thread_update_deletion(
    action,
    thread_update: ThreadUpdate,
    request: HttpRequest | None = None,
) -> bool:
    logger.info(
        "Thread update was deleted",
        extra={
            "id": thread_update.id,
            "user": request.user.id if request else "",
            "ip": request.client_ip if request else "",
        },
    )
    return action(thread_update, request)
```