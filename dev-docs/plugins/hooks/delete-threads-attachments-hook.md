# `delete_threads_attachments_hook`

This hook wraps the standard function that Misago uses to delete attachments associated with specified threads.


## Location

This hook can be imported from `misago.attachments.hooks`:

```python
from misago.attachments.hooks import delete_threads_attachments_hook
```


## Filter

```python
def custom_delete_threads_attachments_filter(
    action: DeleteThreadsAttachmentsHookAction,
    threads: Iterable[Union[Thread, int]],
    *,
    request: HttpRequest | None=None,
) -> int:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: DeleteThreadsAttachmentsHookAction`

A standard function used by Misago to delete attachments associated with specified threads.

See the [action](#action) section for details.


#### `threads: Iterable[Union[Thread, int]]`

An iterable of threads or their IDs.


#### `request: HttpRequest | None`

The request object or `None`.


### Return value

An `int` with the number of attachments marked for deletion.


## Action

```python
def delete_threads_attachments_action(
    threads: Iterable[Union[Thread, int]],
    *,
    request: HttpRequest | None=None,
) -> int:
    ...
```

A standard function used by Misago to delete attachments associated with specified threads.


### Arguments

#### `threads: Iterable[Union[Thread, int]]`

An iterable of threads or their IDs.


#### `request: HttpRequest | None`

The request object or `None`.


### Return value

An `int` with the number of attachments marked for deletion.


## Example

The code below implements a custom filter function that logs delete.

```python
import logging
from typing import Iterable, Protocol, Union

from django.http import HttpRequest
from misago.attachments.hooks import delete_threads_attachments_hook
from misago.threads.models import Thread

logger = logging.getLogger("attachments.delete")


@delete_threads_attachments_hook.append_filter
def log_delete_threads_attachments(
    action,
    threads: Iterable[Union[Thread, int]],
    *,
    request: HttpRequest | None = None,
) -> int:
    deleted = action(threads, request=request)

    if request and request.user.is_authenticated:
        user = f"#{request.user.id}: {request.user.username}"
    else:
        user = None

    logger.info(
        "Deleted threads attachments: %s",
        str(deleted),
        extra={"user": user},
    )

    return deleted
```