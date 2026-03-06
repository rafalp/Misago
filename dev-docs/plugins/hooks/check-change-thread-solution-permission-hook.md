# `check_change_thread_solution_permission_hook`

This hook wraps a standard Misago function used to check whether the user has permission to change the thread’s solution to a new post. Raises `PermissionDenied` with an error message if they don't.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import check_change_thread_solution_permission_hook
```


## Filter

```python
def custom_check_change_thread_solution_permission_filter(
    action: CheckChangeThreadSolutionPermissionHookAction,
    permissions: 'UserPermissionsProxy',
    post: Post,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CheckChangeThreadSolutionPermissionHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `post: Post`

The post to check permissions for.


## Action

```python
def check_change_thread_solution_permission_action(permissions: 'UserPermissionsProxy', post: Post) -> None:
    ...
```

Misago function used to check whether the user has permission to change the thread’s solution to a new post. Raises `PermissionDenied` with an error message if they don't.


### Arguments

#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `post: Post`

The post to check permissions for.


## Example

The code below implements a custom filter function that blocks a user from changing thread's solution if it was selected by an admin.

```python
from django.core.exceptions import PermissionDenied
from django.utils.translation import pgettext
from misago.permissions.hooks import check_change_thread_solution_permission_hook
from misago.permissions.proxy import UserPermissionsProxy
from misago.threads.models import Post

@check_change_thread_solution_permission_hook.append_filter
def check_change_thread_solution_permission(
    action,
    permissions: UserPermissionsProxy,
    post: Post,
) -> None:
    # Run standard permission checks
    action(permissions, post)

    if post.thread.solution_selected_by.is_misago_admin:
        raise PermissionDenied(
            pgettext(
                "solutions permission error",
                "This thread’s solution can't be changed."
            )
        )
```