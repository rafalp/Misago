# `filter_private_thread_posts_queryset_hook`

This hook wraps the standard function that Misago uses set filters on private thread's posts queryset to limit it only to posts that the user can see.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import filter_private_thread_posts_queryset_hook
```


## Filter

```python
def custom_private_thread_posts_queryset_filter(
    action: FilterPrivateThreadPostsQuerysetHookAction,
    permissions: 'UserPermissionsProxy',
    thread: Thread,
    queryset: QuerySet,
) -> QuerySet:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: FilterPrivateThreadPostsQuerysetHookAction`

A standard Misago function used to set filters on a queryset used to retrieve specified private thread's posts that user can see.

See the [action](#action) section for details.


#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `thread: Thread`

A private thread instance which's posts are retrieved.


#### `queryset: Queryset`

A queryset returning thread's posts.


#### Return value

A `queryset` filtered to show only thread posts that the user can see.


## Action

```python
def filter_private_thread_posts_queryset_action(
    permissions: 'UserPermissionsProxy',
    thread: Thread,
    queryset: QuerySet,
) -> QuerySet:
    ...
```

A standard Misago function used to set filters on a queryset used to retrieve specified private thread's posts that user can see.


### Arguments

#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `thread: Thread`

A private thread instance which's posts are retrieved.


#### `queryset: Queryset`

A queryset returning thread's posts.


#### Return value

A `queryset` filtered to show only thread posts that the user can see.


## Example

The code below implements a custom filter function hides deleted posts from anonymous user.

```python
from misago.permissions.hooks import filter_private_thread_posts_queryset_hook
from misago.permissions.proxy import UserPermissionsProxy

@filter_private_thread_posts_queryset_hook.append_filter
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