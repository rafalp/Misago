# `check_see_user_profile_permission_hook`

This hook wraps a Misago function used to check if a user has permission to see another user's profile. Raises Django's PermissionDenied if they don't.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import check_see_user_profile_permission_hook
```


## Filter

```python
def custom_check_see_user_profile_permission_filter(
    action: CheckSeeUserProfilePermissionHookAction,
    permissions: 'UserPermissionsProxy',
    user: 'User',
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CheckSeeUserProfilePermissionHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.

Misago function used to check if a user has permission to see other user's profile. Raises Django's `PermissionDenied` if they don't.


### Arguments

#### `permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `user: User`

The user whose profile is being accessed.


## Action

```python
def check_see_user_profile_permission_action(permissions: 'UserPermissionsProxy', user: 'User') -> None:
    ...
```

Misago function used to check if a user has permission to see another user's profile. Raises Django's PermissionDenied if they don't.


### Arguments

#### `permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `user: User`

The user whose profile is being accessed.


## Example

Block a user from seeing another user's profile if it's private:

```python
from django.core.exceptions import PermissionDenied
from django.utils.translation import pgettext
from misago.permissions.hooks import check_see_user_profile_permission_hook
from misago.permissions.proxy import UserPermissionsProxy
from misago.users.models import User

@check_see_user_profile_permission_hook.append_filter
def check_user_can_see_user_profile(
    action, permissions: UserPermissionsProxy, user: User
) -> None:
    # Run standard permission checks
    action(permissions, user)

    if not user.plugin_data.get("private_profile"):
        return

    if (
        not permissions.user.is_authenticated
        or not permissions.user.plugin_data.get("can_see_private_profiles")
    ):
        raise PermissionDenied(
            pgettext(
                "user profile permission error",
                "%(user)s's profile is private.",
            ) % {"user": user.username}
        )
```