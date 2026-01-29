# `check_edit_private_thread_post_permission_hook`

This hook wraps the standard function that Misago uses to check if the user has permission to edit a post in a private thread. It raises Django's `PermissionDenied` with an error message if they don't.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import check_edit_private_thread_post_permission_hook
```


## Filter

```python
def custom_check_edit_private_thread_post_permission_filter(
    action: CheckEditPrivateThreadPostPermissionHookAction,
    permissions: 'UserPermissionsProxy',
    thread: Thread,
    post: Post,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CheckEditPrivateThreadPostPermissionHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `thread: Thread`

A thread to check permissions for.


#### `post: Post`

A post to check permissions for.


## Action

```python
def check_edit_private_thread_post_permission_action(
    permissions: 'UserPermissionsProxy', thread: Thread, post: Post
) -> None:
    ...
```

Misago function used to check if the user has permission to edit a post in a private thread. It raises Django's `PermissionDenied` with an error message if they don't.


### Arguments

#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `thread: Thread`

A thread to check permissions for.


#### `post: Post`

A post to check permissions for.


## Example

The code below implements a custom filter function that prevents a user from editing a post if it contains a special string.

```python
from django.core.exceptions import PermissionDenied
from misago.categories.models import Category
from misago.permissions.hooks import check_edit_private_thread_post_permission_hook
from misago.permissions.proxy import UserPermissionsProxy
from misago.threads.models import Post, Thread

@check_edit_private_thread_post_permission_hook.append_filter
def check_user_can_edit_thread(
    action,
    permissions: UserPermissionsProxy,
    thread: Thread,
    post: Post,
) -> None:
    action(permissions, thread, post)

    if (
        "[PROTECT]" in post.original
        and not permissions.is_private_threads_moderator
    ):
        raise PermissionError("Only a moderator can edit this post.")
```