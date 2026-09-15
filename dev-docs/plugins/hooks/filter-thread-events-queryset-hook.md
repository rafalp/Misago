# `filter_thread_events_queryset_hook`

This hook wraps the standard function that Misago uses set filters on thread's events queryset to limit it only to events that the user can see.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import filter_thread_events_queryset_hook
```


## Filter

```python
def custom_thread_events_queryset_filter(
    action: FilterThreadEventsQuerysetHookAction,
    permissions: 'UserPermissionsProxy',
    thread: Thread,
    queryset: QuerySet,
) -> QuerySet:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: FilterThreadEventsQuerysetHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `thread: Thread`

A thread instance which's events are retrieved.


#### `queryset: Queryset`

A queryset returning thread's events.


#### Return value

A `QuerySet` filtered to show only thread events that the user can see.


## Action

```python
def filter_thread_events_queryset_action(
    permissions: 'UserPermissionsProxy',
    thread: Thread,
    queryset: QuerySet,
) -> QuerySet:
    ...
```

Misago function used to set filters on a queryset used to retrieve specified thread's events that user can see.


### Arguments

#### `permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `thread: Thread`

A thread instance which's events are retrieved.


#### `queryset: Queryset`

A queryset returning thread's events.


#### Return value

A `QuerySet` filtered to show only thread events that the user can see.


## Example

The code below implements a custom filter function hides all events from anonymous user.

```python
from django.db.models import Queryset
from misago.permissions.hooks import filter_thread_events_queryset_hook
from misago.permissions.proxy import UserPermissionsProxy
from misago.threads.models import Thread

@filter_thread_events_queryset_hook.append_filter
def hide_thread_events_for_anonymous_user(
    action,
    permissions: UserPermissionsProxy,
    thread: Thread,
    queryset: Queryset,
) -> Queryset:
    queryset = action(permissions, thread, queryset)

    if permissions.user.is_anonymous:
        return queryset.none()

    return queryset
```