# `filter_accessible_thread_posts_hook`

This hook wraps a standard Misago function used to set filters on a queryset of posts from   a thread of any type (regular, private, or plugin-specified), limiting it to only the posts that the user can see.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import filter_accessible_thread_posts_hook
```


## Filter

```python
def custom_accessible_thread_posts_filter(
    action: FilterAccessibleThreadPostsHookAction,
    permissions: 'UserPermissionsProxy',
    category: Category,
    thread: Thread,
    queryset: QuerySet,
) -> QuerySet:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: FilterAccessibleThreadPostsHookAction`

Misago function used to set filters on a queryset of posts from a thread of any type (regular, private, or plugin-specified), limiting it to only the posts that the user can see.


#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `category: Category`

A category instance whose posts are being retrieved.


#### `thread: Thread`

A thread instance whose posts are being retrieved.


#### `queryset: Queryset`

A queryset returning the thread's posts.


#### Return value

A `QuerySet` filtered to return only the posts that the user can see.


## Action

```python
def filter_accessible_thread_posts_action(
    permissions: 'UserPermissionsProxy',
    category: Category,
    thread: Thread,
    queryset: QuerySet,
) -> QuerySet:
    ...
```

Misago function used to set filters on a queryset of posts from a thread of any type (regular, private, or plugin-specified), limiting it to only the posts that the user can see.


### Arguments

#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `category: Category`

A category instance whose posts are being retrieved.


#### `thread: Thread`

A thread instance whose posts are being retrieved.


#### `queryset: Queryset`

A queryset returning the thread's posts.


#### Return value

A `QuerySet` filtered to return only the posts that the user can see.


## Example

The code below implements a custom filter function removes hidden posts for anonymous user.

```python
from misago.permissions.hooks import filter_accessible_thread_posts_hook
from misago.permissions.proxy import UserPermissionsProxy

@filter_accessible_thread_posts_hook.append_filter
def exclude_old_private_threads_queryset_hook(
    action,
    permissions: UserPermissionsProxy,
    thread,
    queryset,
) -> None:
    queryset = action(permissions, thread, queryset)

    if permissions.user.is_anonymous:
        return queryset.filter(is_hidden=False)

    return queryset
```