# `create_group_hook`

This hook wraps the standard function that Misago uses to create a new user group.

Misago group creation logic is a thin wrapper for `Group.objects.create()` that updates the `kwargs` to include a valid `slug` generated from the `name` and next valid `ordering` position.

If `kwargs` contains either `request` of `form` special keys, those are also removed before the `create(**kwargs)` is called.


## Location

This hook can be imported from `misago.users.hooks`:

```python
from misago.users.hooks import create_group_hook
```


## Filter

```python
def custom_create_group_filter(action: CreateGroupHookAction, **kwargs) -> Group:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: CreateGroupHookAction`

A standard Misago function used for creating a new user group or the next filter function from another plugin.

See the [action](#action) section for details.


### Additional arguments

In addition to the standard `kwargs` accepted by `Group.objects.create()`, optional arguments may be present:


#### `request: Optional[HttpRequest]`

The request object or `None` if it was not provided.


#### `form: Optional[Form]`

Bound `Form` instance that was used to create this group.


#### `plugin_data: dict`

A plugin data `dict` that will be saved on the `Group.plugin_data` attribute.


### Return value

A newly created `Group` instance.


## Action

```python
def create_group_action(**kwargs) -> Group:
    ...
```

A standard Misago function used for creating a new user group or the next filter function from another plugin.


### Arguments

Accepts the same arguments as `Group.objects.create()`.

It is guaranteed to be called with at least the `name: str` argument.


### Additional arguments

In addition to the standard `kwargs` accepted by `Group.objects.create()`, optional arguments may be present:


#### `request: Optional[HttpRequest]`

The request object or `None` if it was not provided.


#### `form: Optional[Form]`

Bound `Form` instance that was used to create this group.


#### `plugin_data: dict`

A plugin data `dict` that will be saved on the `Group.plugin_data` attribute.


### Return value

A newly created `Group` instance.


## Example

The code below implements a custom filter function that stores an ID of user who created the group, if its available:

```python
from django.http import HttpRequest
from misago.postgres.delete import delete_all
from misago.users.models import Group

@create_group_hook.append_filter
def set_group_creator_id(action, **kwargs) -> Group:
    # request and plugin_data keys are guaranteed to be set in `kwargs`
    if kwargs["request"] and kwargs["request"].user.id:
        kwargs["plugin_data"]["creator_id"] = kwargs["request"].user.id

    # Call the next function in chain
    return action(group, **kwargs)
```