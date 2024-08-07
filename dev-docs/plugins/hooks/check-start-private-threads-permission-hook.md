# `check_start_private_threads_permission_hook`

This hook wraps the standard function that Misago uses to check if the user has a permission to start bew private threads. Raises Django's `PermissionDenied` with an error message if they don't.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import check_start_private_threads_permission_hook
```


## Filter

```python
def custom_check_start_private_threads_permission_filter(
    action: CheckStartPrivateThreadsPermissionHookAction,
    permissions: 'UserPermissionsProxy',
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CheckStartPrivateThreadsPermissionHookAction`

A standard Misago function used to check if the user has a permission to start new private threads. Raises Django's `PermissionDenied` with an error message if they don't.

See the [action](#action) section for details.


#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


## Action

```python
def check_start_private_threads_permission_action(permissions: 'UserPermissionsProxy') -> None:
    ...
```

A standard Misago function used to check if the user has a permission to start new private threads. Raises Django's `PermissionDenied` with an error message if they don't.


### Arguments

#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


## Example

The code below implements a custom filter function that blocks user from starting new private threads if there's a custom flag set on their account.

```python
from django.core.exceptions import PermissionDenied
from django.utils.translation import pgettext
from misago.permissions.hooks import check_start_private_threads_permission_hook
from misago.permissions.proxy import UserPermissionsProxy

@check_start_private_threads_permission_hook.append_filter
def check_user_is_banned_from_starting_private_threads(
    action,
    permissions: UserPermissionsProxy,
) -> None:
    # Run standard permission checks
    action(permissions)

    if permissions.user.plugin_data.get("ban_start_private_threads"):
        raise PermissionDenied(
            pgettext(
                "private threads permission error",
                "Site admin has removed your option to start private threads."
            )
        )
```