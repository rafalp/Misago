# `filter_threads_posts_queryset_hook`

This hook wraps the standard function that Misago uses to filter a queryset to retrieve posts user can see.

This function is usually combined with the filter_threads_queryset to retrieve all posts the user can see from visible threads, e.g. for search results or user activity feeds.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import filter_threads_posts_queryset_hook
```


## Filter

```python
def custom_threads_posts_queryset_filter(
    action: FilterThreadsPostsQuerysetHookAction,
    permissions: 'UserPermissionsProxy',
    categories: list[Union['Category', 'CategoryProxy']],
    queryset: QuerySet | None=None,
) -> QuerySet:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: FilterThreadsPostsQuerysetHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `categories: list[Category|CategoryProxy]`

A list of categories to retrieve posts for.


#### `queryset: Queryset | None = None`

A queryset to filter. If `None`, defaults to `Post.objects`


#### Return value

A `QuerySet` filtered to return only posts that the user can see.


## Action

```python
def filter_threads_posts_queryset_action(
    permissions: 'UserPermissionsProxy',
    categories: list[Union['Category', 'CategoryProxy']],
    queryset: QuerySet | None=None,
) -> QuerySet:
    ...
```

Misago function used to filter a queryset to retrieve posts user can see.


### Arguments

#### `permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `categories: list[Category|CategoryProxy]`

A list of categories to retrieve posts for.


#### `queryset: Queryset | None = None`

A queryset to filter. If `None`, defaults to `Post.objects`


#### Return value

A `QuerySet` filtered to return only posts that the user can see.


## Example

The code below implements a custom filter function that hides too old posts from anonymous user.

```python
from datetime import timedetla

from django.db.models import QuerySet
from django.utils import timezone
from misago.categories.models import Category
from misago.categories.proxy import CategoryProxy
from misago.permissions.hooks import filter_threads_posts_queryset_hook
from misago.permissions.proxy import UserPermissionsProxy

@filter_threads_posts_queryset_hook.append_filter
def exclude_old_posts(
    action,
    permissions: UserPermissionsProxy,
    categories: list[Category | CategoryProxy]
    queryset: QuerySet | None = None,
) -> Queryset:
    queryset = action(permissions, categories, queryset)

    if permissions.user.is_anonymous:
        return queryset.filter(
            posted_at__gt=timezone.now() - timedelta(days=7)
        )

    return queryset
```