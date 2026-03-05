# `check_select_thread_solution_permission_hook`

This hook wraps a standard Misago function used to check whether the user has permission to select a post as the thread’s solution. Raises `PermissionDenied` with an error message if they don't.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import check_select_thread_solution_permission_hook
```


## Filter

```python
def custom_check_select_thread_solution_permission_filter(
    action: CheckSelectThreadSolutionPermissionHookAction,
    permissions: 'UserPermissionsProxy',
    post: Post,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CheckSelectThreadSolutionPermissionHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `post: Post`

The post to check permissions for.


## Action

```python
def check_select_thread_solution_permission_action(permissions: 'UserPermissionsProxy', post: Post) -> None:
    ...
```

Misago function used to check whether the user has permission to select a post as the thread’s solution. Raises `PermissionDenied` with an error message if they don't.


### Arguments

#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `post: Post`

The post to check permissions for.


## Example

The code below implements a custom filter function that blocks a user from selecting a post as a solution if it was posted by a shadow-banned user.

```python
from django.core.exceptions import PermissionDenied
from django.utils.translation import pgettext
from misago.permissions.hooks import check_select_thread_solution_permission_hook
from misago.permissions.proxy import UserPermissionsProxy
from misago.threads.models import Post

@check_select_thread_solution_permission_hook.append_filter
def check_select_thread_solution_permission(
    action,
    permissions: UserPermissionsProxy,
    post: Post,
) -> None:
    # Run standard permission checks
    action(permissions, post)

    if post.poster and post.poster.plugin_data.get("shadow_banned"):
        raise PermissionDenied(
            pgettext(
                "solution permission error",
                "This post can’t be selected as the thread’s solution."
            )
        )
```