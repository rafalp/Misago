# `hide_thread_update_hook`

This hook wraps a standard Misago function used to hide a `ThreadUpdate` object.


## Location

This hook can be imported from `misago.threadupdates.hooks`:

```python
from misago.threadupdates.hooks import hide_thread_update_hook
```


## Filter

```python
def custom_hide_thread_update_filter(
    action: HideThreadUpdateHookAction,
    thread_update: 'ThreadUpdate',
    update_fields: set[str],
    request: HttpRequest | None=None,
) -> bool:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: HideThreadUpdateHookAction`

A standard Misago function used to hide a `ThreadUpdate` object.


#### `thread_update: ThreadUpdate`

A `ThreadUpdate` instance to hide.


#### `update_fields: set[str]`

A `set` of `str` containing the names of fields to pass to the `update(update_fields=...)` option.


#### `request: HttpRequest | None = None`

The request object or `None` if not available.


### Return value

`True` if the thread update was hidden, `False` otherwise.


## Action

```python
def hide_thread_update_action(
    thread_update: 'ThreadUpdate',
    update_fields: set[str],
    request: HttpRequest | None=None,
) -> bool:
    ...
```

A standard Misago function used to hide a `ThreadUpdate` object.


### Arguments

#### `thread_update: ThreadUpdate`

A `ThreadUpdate` instance to hide.


#### `update_fields: set[str]`

A `set` of `str` containing the names of fields to pass to the `update(update_fields=...)` option.


#### `request: HttpRequest | None = None`

The request object or `None` if not available.


### Return value

`True` if the thread update was hidden, `False` otherwise.


## Example

The code below implements a custom filter function that stores the client's IP address when a thread update is hidden:

```python
from django.http import HttpRequest
from misago.threads.hooks import hide_thread_update_hook
from misago.threads.models import ThreadUpdate


@hide_thread_update_hook.append_filter
def save_client_ip_on_thread_update_hide(
    action,
    thread_update: ThreadUpdate,
    update_fields: set[str],
    request: HttpRequest | None = None,
) -> bool:
    if not request:
        return action(thread_update, update_fields)

    thread_update.plugin_data["last_ip"] = request.client_ip
    update_fields.add("plugin_data")

    return action(thread_update, update_fields, request)
```