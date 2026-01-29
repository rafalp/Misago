# `check_delete_post_edit_permission_hook`

This hook wraps the standard Misago function used to check whether a user has permission to delete a post edit. Raises Django's `PermissionDenied` if they don't.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import check_delete_post_edit_permission_hook
```


## Filter

```python
def custom_check_delete_post_edit_permission_filter(
    action: CheckDeletePostEditPermissionHookAction,
    permissions: 'UserPermissionsProxy',
    post_edit: PostEdit,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CheckDeletePostEditPermissionHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `post_edit: PostEdit`

A post edit to check permissions for.


## Action

```python
def check_delete_post_edit_permission_action(
    permissions: 'UserPermissionsProxy', post_edit: PostEdit
) -> None:
    ...
```

Misago function used to check if a user has permission to delete a post edit. Raises Django's `PermissionDenied` if they don't.


### Arguments

#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `post_edit: PostEdit`

A post edit to check permissions for.


## Example

The code below implements a custom filter function that blocks a user from deleting a post edit record if it has a protected flag.

```python
from django.core.exceptions import PermissionDenied
from django.utils.translation import pgettext
from misago.edits.models import PostEdit
from misago.permissions.hooks import check_delete_post_edit_permission_hook
from misago.permissions.proxy import UserPermissionsProxy

@check_delete_post_edit_permission_hook.append_filter
def check_user_can_delete_protected_post_edit(
    action,
    permissions: UserPermissionsProxy,
    post_edit: PostEdit,
) -> None:
    # Run standard permission checks
    action(permissions, post_edit)

    if post_edit.plugin_data.get("is_protected"):
        raise PermissionDenied(
            pgettext(
                "edits permission error",
                "You can't delete this post edit."
            )
        )
```