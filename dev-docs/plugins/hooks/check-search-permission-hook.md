# `check_search_permission_hook`

This hook wraps the standard function that Misago uses to check if the user has permission to search the site. Raises Django's `PermissionDenied` with an error message if they don't.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import check_search_permission_hook
```


## Filter

```python
def custom_check_search_permission_filter(
    action: CheckPrivateThreadsPermissionHookAction,
    permissions: 'UserPermissionsProxy',
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CheckPrivateThreadsPermissionHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


## Action

```python
def check_search_permission_action(permissions: 'UserPermissionsProxy') -> None:
    ...
```

Misago function used to check if the user has permission to search the site. Raises Django's `PermissionDenied` with an error message if they don't.


### Arguments

#### `permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


## Example

The code below implements a custom filter function that blocks user from searching the site if their IP address is banned.

```python
from django.core.exceptions import PermissionDenied
from django.utils.translation import pgettext
from misago.users.bans import get_request_ip_ban
from misago.permissions.hooks import check_search_permission_hook
from misago.permissions.proxy import UserPermissionsProxy

@check_search_permission_hook.append_filter
def check_user_can_search_permission(
    action,
    permissions: UserPermissionsProxy,
) -> None:
    # Run standard permission checks
    action(permissions)

    if get_request_ip_ban(request):
        raise PermissionDenied(
            pgettext(
                "search permission error",
                "You can't search this site."
            )
        )
```