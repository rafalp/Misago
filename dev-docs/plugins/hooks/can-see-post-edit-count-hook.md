# `can_see_post_edit_count_hook`

This hook wraps a standard Misago function used to check if a user has permission to see a post's edit count. Returns `True` if they can and `False` if they don't.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import can_see_post_edit_count_hook
```


## Filter

```python
def custom_can_see_post_edit_count_filter(
    action: CanSeePostsEditCountHookAction,
    permissions: 'UserPermissionsProxy',
    category: Category,
    thread: Thread,
    post: Post,
) -> bool:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CanSeePostsEditCountHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `users: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `category: Category`

A category to check permissions for.


#### `thread: Thread`

A thread to check permissions for.


#### `post: Post`

A post to check permissions for.


### Return value

A `bool` with `True` if user can see post's edit count, and `False` if they can't.


## Action

```python
def can_see_post_edit_count_action(
    permissions: 'UserPermissionsProxy',
    category: Category,
    thread: Thread,
    post: Post,
) -> bool:
    ...
```

Misago function used to check if a user has permission to see a post's edit count. Returns `True` if they can and `False` if they don't.


### Arguments

#### `users: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `category: Category`

A category to check permissions for.


#### `thread: Thread`

A thread to check permissions for.


#### `post: Post`

A post to check permissions for.


### Return value

A `bool` with `True` if user can see post's edit count, and `False` if they can't.


## Example

The code below implements a custom filter function that blocks a user from seeing a specific post's edit count if it has a flag.

```python
from django.core.exceptions import PermissionDenied
from django.utils.translation import pgettext
from misago.categories.models import Category
from misago.permissions.hooks import can_see_post_edit_count_hook
from misago.permissions.proxy import UserPermissionsProxy
from misago.threads.models import Post, Thread

@can_see_post_edit_count_hook.append_filter
def check_user_can_see_post_edits(
    action,
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
    post: Post,
) -> bool:
    if post.plugin_data.get("hide_edits"):
        return False

    return action(permissions, category, thread, post)
```