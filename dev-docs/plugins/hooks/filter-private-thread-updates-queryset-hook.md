# `filter_private_thread_updates_queryset_hook`

This hook wraps the standard function that Misago uses set filters on private thread's updates queryset to limit it only to updates that the user can see.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import filter_private_thread_updates_queryset_hook
```


## Filter

```python
def custom_private_thread_updates_queryset_filter(
    action: FilterPrivateThreadUpdatesQuerysetHookAction,
    permissions: 'UserPermissionsProxy',
    thread: Thread,
    queryset: QuerySet,
) -> QuerySet:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: FilterPrivateThreadUpdatesQuerysetHookAction`

Misago function used to set filters on a queryset used to retrieve specified private thread's updates that user can see.

See the [action](#action) section for details.


#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `thread: Thread`

A private thread instance which's updates are retrieved.


#### `queryset: Queryset`

A queryset returning thread's updates.


#### Return value

A `queryset` filtered to show only thread updates that the user can see.


## Action

```python
def filter_private_thread_updates_queryset_action(
    permissions: 'UserPermissionsProxy',
    thread: Thread,
    queryset: QuerySet,
) -> QuerySet:
    ...
```

Misago function used to set filters on a queryset used to retrieve specified private thread's updates that user can see.


### Arguments

#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `thread: Thread`

A private thread instance which's updates are retrieved.


#### `queryset: Queryset`

A queryset returning thread's updates.


#### Return value

A `queryset` filtered to show only thread updates that the user can see.


## Example

The code below implements a custom filter function hides updates user who is not the private thread's owner.

```python
from misago.permissions.hooks import filter_private_thread_updates_queryset_hook
from misago.permissions.proxy import UserPermissionsProxy

@filter_private_thread_updates_queryset_hook.append_filter
def hide_private_thread_updates_from_non_owner(
    action,
    permissions: UserPermissionsProxy,
    thread,
    queryset,
) -> None:
    queryset = action(permissions, thread, queryset)

    if permissions.user.id != thread.private_thread_owner_id:
        return queryset.none()

    return queryset
```