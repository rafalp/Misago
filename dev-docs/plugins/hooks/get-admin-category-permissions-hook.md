# `get_admin_category_permissions_hook`

This hook lets plugins add permissions to Admin Category Permissions forms.


## Location

This hook can be imported from `misago.permissions.hooks`:

```python
from misago.permissions.hooks import get_admin_category_permissions_hook
```


## Action

```python
def custom_get_admin_category_permissions_filter(form: PermissionsFormView) -> list[dict]:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `form: PermissionsFormView`

An instance of Admin Category Permissions Form view that implements a `create_permission` factory function that plugin should use to create new permissions.


#### Return value

A list of Python `dict`s with permissions to include in Admin Category Permissions Form.


## Example

The code below implements a custom action that adds `BUMP` and `BURY` permissions to category permission forms:

```python
from misago.admin.views.generic import PermissionsFormView
from misago.permissions.hooks import get_admin_category_permissions_hook


@get_admin_category_permissions_hook.append_action
def add_plugin_category_permissions(form: PermissionsFormView) -> list[dict]:
    return [
        form.create_permission(
            id="BUMP",
            name="Bump threads",
            help_text="Allows users to bump threads."
            color="#ecfeff",
        ),
        form.create_permission(
            id="BURY",
            name="Bury threads",
            help_text="Allows users to bury threads."
            color="#f5f3ff",
        ),
    ]
```

To create a `dict` with permission's data, you should use the `create_permission` method from the `form` instance:

```python
def create_permission(
    id: str, name: str, help_text: str | None = None, , color: str | None = None
) -> dict:
    ...
```