# `check_like_post_permission_hook`

This hook wraps a standard Misago function used to check if a user has permission to like a post. Raises Django's `PermissionDenied` if they don't.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import check_like_post_permission_hook
```


## Filter

```python
def custom_check_like_post_permission_filter(
    action: CheckLikePostPermissionHookAction,
    permissions: 'UserPermissionsProxy',
    category: Category,
    thread: Thread,
    post: Post,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CheckLikePostPermissionHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `category: Category`

A category to check permissions for.


#### `thread: Thread`

A thread to check permissions for.


#### `post: Post`

A post to check permissions for.


## Action

```python
def check_like_post_permission_action(
    permissions: 'UserPermissionsProxy',
    category: Category,
    thread: Thread,
    post: Post,
) -> None:
    ...
```

Misago function used to check if a user has permission to like a post. Raises Django's `PermissionDenied` if they don't.


### Arguments

#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `category: Category`

A category to check permissions for.


#### `thread: Thread`

A thread to check permissions for.


#### `post: Post`

A post to check permissions for.


## Example

The code below implements a custom filter function that blocks a user from liking a specific post if there is a custom flag set on it.

```python
from django.core.exceptions import PermissionDenied
from django.utils.translation import pgettext
from misago.categories.models import Category
from misago.permissions.hooks import check_like_post_permission_hook
from misago.permissions.proxy import UserPermissionsProxy
from misago.threads.models import Post, Thread

@check_like_post_permission_hook.append_filter
def check_user_can_like_post(
    action,
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
    post: Post,
) -> None:
    # Run standard permission checks
    action(permissions, category, thread, post)

    if post.plugin_data.get("disable_likes"):
        raise PermissionDenied(
            pgettext(
                "post permission error",
                "You can't like this post."
            )
        )
```