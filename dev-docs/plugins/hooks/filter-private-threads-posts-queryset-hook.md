# `filter_private_threads_posts_queryset_hook`

This hook wraps the standard function that Misago uses to filter a queryset to retrieve private threads posts the user can see.

This function is usually combined with the `filter_private_threads_queryset` to retrieve all posts the user can see from visible threads, e.g. for search results.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import filter_private_threads_posts_queryset_hook
```


## Filter

```python
def custom_private_threads_posts_queryset_filter(
    action: FilterPrivateThreadsPostsQuerysetHookAction,
    permissions: 'UserPermissionsProxy',
    queryset: QuerySet,
) -> QuerySet:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: FilterPrivateThreadsPostsQuerysetHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `queryset: Queryset`

A queryset returning posts.


#### Return value

A `QuerySet` filtered to show only thread posts that the user can see.


## Action

```python
def filter_private_threads_posts_queryset_action(
    permissions: 'UserPermissionsProxy', queryset: QuerySet
) -> QuerySet:
    ...
```

Misago function used to filter a queryset to retrieve private threads posts the user can see.


### Arguments

#### `permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `queryset: Queryset`

A queryset returning posts.


#### Return value

A `QuerySet` filtered to show only thread posts that the user can see.


## Example

The code below implements a custom filter function that hides too old posts from the user.

```python
from datetime import timedetla

from django.db.models import QuerySet
from django.utils import timezone
from misago.permissions.hooks import filter_private_threads_posts_queryset_hook
from misago.permissions.proxy import UserPermissionsProxy

@filter_private_threads_posts_queryset_hook.append_filter
def exclude_old_posts(
    action,
    permissions: UserPermissionsProxy,
    queryset: QuerySet | None = None,
) -> Queryset:
    queryset = action(permissions, queryset)

    if permissions.is_private_threads_moderator:
        return queryset

    return queryset.filter(
        posted_at__gt=timezone.now() - timedelta(days=7)
    )
```