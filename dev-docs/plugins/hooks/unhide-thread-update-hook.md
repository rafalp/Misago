# `unhide_thread_update_hook`

This hook wraps a standard Misago function used to unhide a `ThreadUpdate` object.


## Location

This hook can be imported from `misago.threadevents.hooks`:

```python
from misago.threadevents.hooks import unhide_thread_update_hook
```


## Filter

```python
def custom_unhide_thread_update_filter(
    action: UnhideThreadUpdateHookAction,
    thread_update: 'ThreadUpdate',
    request: HttpRequest | None=None,
) -> bool:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: UnhideThreadUpdateHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `thread_update: ThreadUpdate`

A `ThreadUpdate` instance to unhide.


#### `request: HttpRequest | None = None`

The request object or `None` if not available.


### Return value

`True` if the thread update was unhidden, `False` otherwise.


## Action

```python
def unhide_thread_update_action(
    thread_update: 'ThreadUpdate', request: HttpRequest | None=None
) -> bool:
    ...
```

Misago function used to unhide a `ThreadUpdate` object.


### Arguments

#### `thread_update: ThreadUpdate`

A `ThreadUpdate` instance to unhide.


#### `request: HttpRequest | None = None`

The request object or `None` if not available.


### Return value

`True` if the thread update was unhidden, `False` otherwise.


## Example

The code below implements a custom filter function that stores the client's IP address when a thread update is unhidden:

```python
from django.http import HttpRequest
from misago.threads.hooks import unhide_thread_update_hook
from misago.threads.models import ThreadUpdate


@unhide_thread_update_hook.append_filter
def save_client_ip_on_thread_update_unhide(
    action,
    thread_update: ThreadUpdate,
    request: HttpRequest | None = None,
) -> bool:
    if not request:
        return action(thread_update)

    thread_update.plugin_data["last_ip"] = request.client_ip

    return action(thread_update, request)
```