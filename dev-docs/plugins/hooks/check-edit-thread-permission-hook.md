# `check_edit_thread_permission_hook`

This hook wraps the standard function that Misago uses to check if the user has permission to edit a thread. It raises Django's `PermissionDenied` with an error message if they can't edit it.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import check_edit_thread_permission_hook
```


## Filter

```python
def custom_check_edit_thread_permission_filter(
    action: CheckEditThreadPermissionHookAction,
    permissions: 'UserPermissionsProxy',
    category: Category,
    thread: Thread,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CheckEditThreadPermissionHookAction`

A standard Misago function used to check if the user has permission to edit a thread. It raises Django's `PermissionDenied` with an error message if they can't edit it.

See the [action](#action) section for details.


#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `category: Category`

A category to check permissions for.


#### `thread: Thread`

A thread to check permissions for.


## Action

```python
def check_edit_thread_permission_action(
    permissions: 'UserPermissionsProxy',
    category: Category,
    thread: Thread,
) -> None:
    ...
```

A standard Misago function used to check if the user has permission to edit a thread. It raises Django's `PermissionDenied` with an error message if they can't edit it.


### Arguments

#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `category: Category`

A category to check permissions for.


#### `thread: Thread`

A thread to check permissions for.


## Example

The code below implements a custom filter function that prevents a user from editing a thread if it's title contains a special prefix.

```python
from django.core.exceptions import PermissionDenied
from misago.categories.models import Category
from misago.permissions.hooks import check_edit_thread_permission_hook
from misago.permissions.proxy import UserPermissionsProxy
from misago.threads.models import Thread

@check_edit_thread_permission_hook.append_filter
def check_user_can_edit_thread(
    action,
    permissions: UserPermissionsProxy,
    category: Category,
    thread: Thread,
) -> None:
    action(permissions, category, thread)

    if (
        thread.title.startswith("[MVP]")
        and not (
            permissions.is_global_moderator
            or permissions.is_category_moderator(thread.category_id)
        )
    ):
        raise PermissionError("Only a moderator can edit this thread.")
```