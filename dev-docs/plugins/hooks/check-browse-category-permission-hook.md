# `check_browse_category_permission_hook`

This hook wraps the standard function that Misago uses to check if the user has permission to browse a category. It also checks if the user can see the category. It raises Django's `Http404` if they can't see it or `PermissionDenied` with an error message if they can't browse it.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import check_browse_category_permission_hook
```


## Filter

```python
def custom_check_browse_category_permission_filter(
    action: CheckBrowseCategoryPermissionHookAction,
    permissions: 'UserPermissionsProxy',
    category: Category,
    can_delay: bool=False,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CheckBrowseCategoryPermissionHookAction`

A standard Misago function used to check if the user has permission to browse a category. It also checks if the user can see the category. It raises Django's `Http404` if they can't see it or `PermissionDenied` with an error message if they can't browse it.

See the [action](#action) section for details.


#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `category: Category`

A category to check permissions for.


#### `can_delay: Bool = False`

A `bool` that specifies if this check can be delayed. If the category can be seen by the user but they have no permission to browse it, and both `can_delay` and `category.delay_browse_check` are `True`, a `PermissionDenied` error will not be raised.


## Action

```python
def check_browse_category_permission_action(
    permissions: 'UserPermissionsProxy',
    category: Category,
    can_delay: bool=False,
) -> None:
    ...
```

A standard Misago function used to check if the user has permission to browse a category. It also checks if the user can see the category. It raises Django's `Http404` if they can't see it or `PermissionDenied` with an error message if they can't browse it.


### Arguments

#### `user_permissions: UserPermissionsProxy`

A proxy object with the current user's permissions.


#### `category: Category`

A category to check permissions for.


#### `can_delay: Bool = False`

A `bool` that specifies if this check can be delayed. If the category can be seen by the user but they have no permission to browse it, and both `can_delay` and `category.delay_browse_check` are `True`, a `PermissionDenied` error will not be raised.


## Example

The code below implements a custom filter function that blocks a user from browsing a specified category if there is a custom flag set on their account.

```python
from django.core.exceptions import PermissionDenied
from django.utils.translation import pgettext
from misago.categories.models import Category
from misago.permissions.hooks import check_browse_category_permission_hook
from misago.permissions.proxy import UserPermissionsProxy

@check_browse_category_permission_hook.append_filter
def check_user_can_browse_category(
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