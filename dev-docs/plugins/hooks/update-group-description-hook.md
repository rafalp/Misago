# `update_group_description_hook`

This hook wraps the standard function that Misago uses to update user group's description.


## Location

This hook can be imported from `misago.users.hooks`:

```python
from misago.users.hooks import update_group_description_hook
```


## Filter

```python
def custom_update_group_description_filter(
    action: UpdateGroupDescriptionHookAction, group: Group, **kwargs
) -> Group:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: UpdateGroupDescriptionHookAction`

A standard Misago function used to update an existing user group's description or the next filter function from another plugin.

See the [action](#action) section for details.


#### `group: Group`

A group instance to update.


#### `**kwargs`

A `dict` with group description's attributes to update.


### Additional arguments

Optional arguments in `kwargs` that are not used to update the group but are still provided for use by plugins:


#### `request: Optional[HttpRequest]`

The request object or `None` if it was not provided.


#### `form: Optional[Form]`

Bound `Form` instance that was used to update this group's description.


### Return value

An updated `Group` instance.


## Action

```python
def update_group_description_action(group: Group, **kwargs) -> Group:
    ...
```

A standard Misago function used to update an existing user group's description or the next filter function from another plugin.


### Arguments

#### `group: Group`

A group instance to update.


#### `**kwargs`

A `dict` with group description's attributes to update.


### Additional arguments

Optional arguments in `kwargs` that are not used to update the group but are still provided for use by plugins:


#### `request: Optional[HttpRequest]`

The request object or `None` if it was not provided.


#### `form: Optional[Form]`

Bound `Form` instance that was used to update this group's description.


### Return value

An updated `Group` instance.


## Example

The code below implements a custom filter function that stores an ID of user who last modified the group description, if its available:

```python
from django.http import HttpRequest
from misago.users.models import Group

@update_group_description_hook.append_filter
def set_group_description_updated_by_id(action, **kwargs) -> Group:
    # request key is guaranteed to be set in `kwargs`
    if kwargs["request"] and kwargs["request"].user.id:
        group.description.plugin_data["updated_by"] = kwargs["request"].user.id

    # Call the next function in chain
    return action(group, **kwargs)
```