# `create_thread_event_hook`

This hook wraps a standard Misago function used to create a `ThreadEvent` object.


## Location

This hook can be imported from `misago.threadevents.hooks`:

```python
from misago.threadevents.hooks import create_thread_event_hook
```


## Filter

```python
def custom_create_thread_event_filter(
    action: CreateThreadEventHookAction,
    thread: 'Thread',
    event_type: str,
    actor: Union['User', None, str]=None,
    *,
    context: str | None=None,
    context_object: Model | None=None,
    context_items: int | None=None,
    commit: bool=True,
    request: HttpRequest | None=None,
) -> 'ThreadEvent':
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CreateThreadEventHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `thread: Thread`

A `Thread` instance.


#### `event_type: str`

A `str` with the name of the event type.


#### `actor: Union["User", None, str] = None`

The actor who performed the action: a `User` instance, a `str` with a name, or `None` if not available.


#### `context: str | None = None`

A `str` with context, e.g., a previous thread title or the name of `context_object`. `None` if not available or not used for this `event_type`.


#### `context_object: Model | None = None`

A `Model` instance that this event object should store a generic relation to.


#### `context_items: int | None = None`

A number of items affected by the event.


#### `commit: bool = True`

A `bool` indicating whether the new `ThreadEvent` instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None = None`

The request object or `None` if not available.


### Return value

A newly created `ThreadEvent` instance.


## Action

```python
def create_thread_event_action(
    thread: 'Thread',
    event_type: str,
    actor: Union['User', None, str]=None,
    *,
    context: str | None=None,
    context_object: Model | None=None,
    context_items: int | None=None,
    commit: bool=True,
    request: HttpRequest | None=None,
) -> 'ThreadEvent':
    ...
```

Misago function used to create a `ThreadEvent` object.


### Arguments

#### `thread: Thread`

A `Thread` instance.


#### `event_type: str`

A `str` with the name of the event type.


#### `actor: Union["User", None, str] = None`

The actor who performed the action: a `User` instance, a `str` with a name, or `None` if not available.


#### `context: str | None = None`

A `str` with context, e.g., a previous thread title or the name of `context_object`. `None` if not available or not used for this `event_type`.


#### `context_object: Model | None = None`

A `Model` instance that this event object should store a generic relation to.


#### `context_items: int | None = None`

A number of items affected by the event.


#### `commit: bool = True`

A `bool` indicating whether the new `ThreadEvent` instance should be saved to the database.

Defaults to `True`.


#### `request: HttpRequest | None = None`

The request object or `None` if not available.


### Return value

A newly created `ThreadEvent` instance.


## Example

The code below implements a custom filter function that stores the actor's IP address on the thread event object:

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
) -> ThreadEvent:
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