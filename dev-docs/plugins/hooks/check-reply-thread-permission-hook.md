# `check_reply_thread_permission_hook`

This hook wraps the standard function that Misago uses to check if the user has permission to reply to a thread. It raises Django's `PermissionDenied` with an error message if they can't post in it.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import check_reply_thread_permission_hook
```


## Filter

```python
def custom_check_reply_thread_permission_filter(
    action: CheckReplyThreadPermissionHookAction,
    permissions: 'UserPermissionsProxy',
    category: Category,
    thread: Thread,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CheckReplyThreadPermissionHookAction`

A standard Misago function used to check if the user has permission to reply to a thread. It raises Django's `PermissionDenied` with an error message if they can't reply to it.

See the [action](#action) section for details.


#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `category: Category`

A category to check permissions for.


#### `thread: Thread`

A thread to check permissions for.


## Action

```python
def check_reply_thread_permission_action(
    permissions: 'UserPermissionsProxy',
    category: Category,
    thread: Thread,
) -> None:
    ...
```

A standard Misago function used to check if the user has permission to reply to a thread. It raises Django's `PermissionDenied` with an error message if they can't reply to it.


### Arguments

#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `category: Category`

A category to check permissions for.


#### `thread: Thread`

A thread to check permissions for.


## Example

The code below implements a custom filter function that prevents a user from replying to a thread if they are a thread starter, but only in categories with a plugin flag.

```python
from django.core.exceptions import PermissionDenied
from misago.categories.models import Category
from misago.permissions.hooks import check_reply_thread_permission_hook
from misago.permissions.proxy import UserPermissionsProxy
from misago.threads.models import Thread

@check_reply_thread_permission_hook.append_filter
def check_user_can_reply_in_thread(
    action,
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
) -> None:
    user = permissions.user
    if (
        category.plugin_data.get("block_starters")
        and user.is_authenticated and user.id == thread.starter_id
    ):
        raise PermissionDenied("You can't reply to threads you've started.")

    action(permissions, category, thread)
```