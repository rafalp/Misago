# `hide_thread_event_hook`

This hook wraps a standard Misago function used to hide a `ThreadUpdate` object.


## Location

This hook can be imported from `misago.threadevents.hooks`:

```python
from misago.threadevents.hooks import hide_thread_event_hook
```


## Filter

```python
def custom_hide_thread_event_filter(
    action: HideThreadUpdateHookAction,
    thread_event: 'ThreadUpdate',
    request: HttpRequest | None=None,
) -> bool:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: HideThreadUpdateHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `thread_event: ThreadUpdate`

A `ThreadUpdate` instance to hide.


#### `request: HttpRequest | None = None`

The request object or `None` if not available.


### Return value

`True` if the thread update was hidden, `False` otherwise.


## Action

```python
def hide_thread_event_action(
    thread_event: 'ThreadUpdate', request: HttpRequest | None=None
) -> bool:
    ...
```

Misago function used to hide a `ThreadUpdate` object.


### Arguments

#### `thread_event: ThreadUpdate`

A `ThreadUpdate` instance to hide.


#### `request: HttpRequest | None = None`

The request object or `None` if not available.


### Return value

`True` if the thread update was hidden, `False` otherwise.


## Example

The code below implements a custom filter function that stores the client's IP address when a thread update is hidden:

```python
from django.http import HttpRequest
from misago.threads.hooks import hide_thread_event_hook
from misago.threads.models import ThreadUpdate


@hide_thread_event_hook.append_filter
def save_client_ip_on_thread_event_hide(
    action,
    thread_event: ThreadUpdate,
    request: HttpRequest | None = None,
) -> bool:
    if not request:
        return action(thread_event)

    thread_event.plugin_data["last_ip"] = request.client_ip

    return action(thread_event, request)
```