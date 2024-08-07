# `check_post_in_closed_category_permission_hook`

This hook wraps the standard function that Misago uses to check if the user has permission to post in a closed category. It raises Django's `PermissionDenied` with an error message if category is closed and they can't post in it.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import check_post_in_closed_category_permission_hook
```


## Filter

```python
def custom_check_post_in_closed_category_permission_filter(
    action: CheckPostInClosedCategoryPermissionHookAction,
    permissions: 'UserPermissionsProxy',
    category: Category,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CheckPostInClosedCategoryPermissionHookAction`

A standard Misago function used to check if the user has permission to post in a closed category. It raises Django's `PermissionDenied` with an error message if category is closed and they can't post in it.

See the [action](#action) section for details.


#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `category: Category`

A category to check permissions for.


## Action

```python
def check_post_in_closed_category_permission_action(
    permissions: 'UserPermissionsProxy', category: Category
) -> None:
    ...
```

A standard Misago function used to check if the user has permission to post in a closed category. It raises Django's `PermissionDenied` with an error message if category is closed and they can't post in it.


### Arguments

#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `category: Category`

A category to check permissions for.


## Example

The code below implements a custom filter function that permits a user to post in the specific category if they have a custom flag set on their account.

```python
from misago.categories.models import Category
from misago.permissions.hooks import check_post_in_closed_category_permission_hook
from misago.permissions.proxy import UserPermissionsProxy

@check_post_in_closed_category_permission_hook.append_filter
def check_user_can_post_in_closed_category(
    action,
    permissions: UserPermissionsProxy,
    category: Category,
) -> None:
    user = permissions.user
    if user.is_authenticated:
        post_in_closed_categories = (
            user.plugin_data.get("post_in_closed_categories") or []
        )
    else:
        post_in_closed_categories = None

    if (
        not post_in_closed_categories
        or category.id not in post_in_closed_categories
    ):
        action(permissions, category)
```