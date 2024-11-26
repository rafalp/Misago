# `filter_private_threads_queryset_hook`

This hook wraps the standard function that Misago uses set filters on a private threads queryset to limit it only to threads that the user has access to.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import filter_private_threads_queryset_hook
```


## Filter

```python
def custom_private_threads_queryset_filter(
    action: FilterPrivateThreadsQuerysetHookAction,
    permissions: 'UserPermissionsProxy',
    queryset: QuerySet,
) -> QuerySet:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: FilterPrivateThreadsQuerysetHookAction`

A standard Misago function used to set filters on a private threads queryset to limit it only to threads that the user has access to.

See the [action](#action) section for details.


#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `queryset: Queryset`

A queryset returning all private threads.


#### Return value

A `queryset` filtered to show only private threads that the user has access to.


## Action

```python
def filter_private_threads_queryset_action(
    permissions: 'UserPermissionsProxy', queryset: QuerySet
) -> QuerySet:
    ...
```

A standard Misago function used to set filters on a private threads queryset to limit it only to threads that the user has access to.


### Arguments

#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `queryset: Queryset`

A queryset returning all private threads.


#### Return value

A `queryset` filtered to show only private threads that the user has access to.


## Example

The code below implements a custom filter function that makes old private threads not available to the user.

```python
from datetime import timedelta

from django.utils import timezone
from misago.permissions.hooks import filter_private_threads_queryset_hook
from misago.permissions.proxy import UserPermissionsProxy

@filter_private_threads_queryset_hook.append_filter
def exclude_old_private_threads_queryset_hook(
    action,
    permissions: UserPermissionsProxy,
    queryset,
) -> None:
   queryset = action(permissions, queryset)

    if permissions.is_private_threads_moderator:
       return queryset

    return queryset.filter(
        last_post_on__gt=timezone.now - timedelta(days=30),
    )
```