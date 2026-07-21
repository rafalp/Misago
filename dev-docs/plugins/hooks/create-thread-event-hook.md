# `create_thread_event_hook`

This hook wraps a standard Misago function used to create a `ThreadUpdate` object.


## Location

This hook can be imported from `misago.threadevents.hooks`:

```python
from misago.threadevents.hooks import create_thread_event_hook
```


## Filter

```python
def custom_create_thread_event_filter(
    action: CreateThreadUpdateHookAction,
    thread: 'Thread',
    action_name: str,
    actor: Union['User', None, str]=None,
    *,
    context: str | None=None,
    context_object: Model | None=None,
    context_items: int | None=None,
    commit: bool=True,
    request: HttpRequest | None=None,
) -> 'ThreadUpdate':
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CreateThreadUpdateHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `thread: Thread`

A `Thread` instance.


#### `action_name: str`

A `str` with the name of the action that updated the thread.


#### `actor: Union["User", None, str] = None`

The actor who performed the action: a `User` instance, a `str` with a name, or `None` if not available.


#### `context: str | None = None`

A `str` with context, e.g., a previous thread title or the name of `context_object`. `None` if not available or not used for this `action_name`.


#### `context_object: Model | None = None`

A `Model` instance that this update object should store a generic relation to.


#### `context_items: int | None = None`

A number of items affected by the event.


#### `commit: bool = True`

A `bool` indicating whether the new `ThreadUpdate` instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None = None`

The request object or `None` if not available.


### Return value

A newly created `ThreadUpdate` instance.


## Action

```python
def create_thread_event_action(
    thread: 'Thread',
    action_name: str,
    actor: Union['User', None, str]=None,
    *,
    context: str | None=None,
    context_object: Model | None=None,
    context_items: int | None=None,
    commit: bool=True,
    request: HttpRequest | None=None,
) -> 'ThreadUpdate':
    ...
```

Misago function used to create a `ThreadUpdate` object.


### Arguments

#### `thread: Thread`

A `Thread` instance.


#### `action_name: str`

A `str` with the name of the action that updated the thread.


#### `actor: Union["User", None, str] = None`

The actor who performed the action: a `User` instance, a `str` with a name, or `None` if not available.


#### `context: str | None = None`

A `str` with context, e.g., a previous thread title or the name of `context_object`. `None` if not available or not used for this `action_name`.


#### `context_object: Model | None = None`

A `Model` instance that this update object should store a generic relation to.


#### `context_items: int | None = None`

A number of items affected by the event.


#### `commit: bool = True`

A `bool` indicating whether the new `ThreadUpdate` instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None = None`

The request object or `None` if not available.


### Return value

A newly created `ThreadUpdate` instance.


## Example

The code below implements a custom filter function that stores the actor's IP address on the update object:

```python
from django.http import HttpRequest
from misago.threadevents.hooks import create_thread_event_hook
from misago.threadevents.models import ThreadEvent


@create_thread_event_hook.append_filter
def set_actor_ip_on_thread_event(
    action,
    *args,
    commit: bool = True,
    request: HttpRequest | None = None,
    **kwargs
) -> ThreadUpdate:
    if request:
        plugin_data["actor_id"] = request.user_ip

    thread_event = action(
        *args,
        commit=False,
        request=request,
        **kwargs
    )

    if request:
        thread_event.plugin_data["actor_id"] = request.user_ip

    if commit:
        thread_event.save()

    return thread_event
```