# `check_see_category_permission_hook`

This hook wraps the standard function that Misago uses to check if the user has a permission to see a category. Raises Django's `Http404` error if they don't.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import check_see_category_permission_hook
```


## Filter

```python
def custom_check_see_category_permission_filter(
    action: CheckSeeCategoryPermissionHookAction,
    permissions: 'UserPermissionsProxy',
    category: Category,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CheckSeeCategoryPermissionHookAction`

A standard Misago function used to check if the user has a permission to see a category. Raises Django's `Http404` error if they don't.

See the [action](#action) section for details.


#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `category: Category`

A category to check permissions for.


## Action

```python
def check_see_category_permission_action(
    permissions: 'UserPermissionsProxy', category: Category
) -> None:
    ...
```

A standard Misago function used to check if the user has a permission to see a category. Raises Django's `Http404` error if they don't.


### Arguments

#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `category: Category`

A category to check permissions for.


## Example

The code below implements a custom filter function that blocks a user from seeing a specified category if there is a custom flag set on their account.

```python
from django.core.exceptions import PermissionDenied
from django.utils.translation import pgettext
from misago.categories.models import Category
from misago.permissions.hooks import check_see_category_permission_hook
from misago.permissions.proxy import UserPermissionsProxy

@check_see_category_permission_hook.append_filter
def check_user_can_see_category(
    action,
    permissions: UserPermissionsProxy,
    category: Category,
) -> None:
    # Run standard permission checks
    action(permissions, category)

    if category.id in permissions.user.plugin_data.get("banned_categories", []):
        raise PermissionDenied(
            pgettext(
                "category permission error",
                "Site admin has removed your access to this category."
            )
        )
```