# `set_default_group_hook`

This hook wraps the standard function that Misago uses to set a default user group.

The default user group is the group assigned to a user at account creation time.


## Location

This hook can be imported from `misago.users.hooks`:

```python
from misago.users.hooks import set_default_group_hook
```


## Filter

```python
def custom_set_default_group_filter(
    action: SetDefaultGroupHookAction,
    group: Group,
    request: HttpRequest | None=None,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: SetDefaultGroupHookAction`

A standard Misago function used to set the default user group, or the next filter function from another plugin.

See the [action](#action) section for details.


#### `group: Group`

A `Group` model instance to set as default in the database.


#### `request: Optional[HttpRequest]`

The request object or `None` if it was not provided.


## Action

```python
def set_default_group_action(group: Group, request: HttpRequest | None=None) -> None:
    ...
```

A standard Misago function used to set the default user group, or the next filter function from another plugin.


### Arguments

#### `group: Group`

A `Group` model instance to set as default in the database.


#### `request: Optional[HttpRequest]`

The request object or `None` if it was not provided.


## Example

The code below implements a custom filter function that logs the default group change:

```python
from logging import getLogger

from django.http import HttpRequest
from misago.users.models import Group

logger = getLogger(__file__)

@set_default_group_hook.append_filter
def log_default_group_change(
    action, group: Group, request: HttpRequest | None = None
) -> None:
    if request:
        logger.info(
            "%s (#%s) changed default user group to %s (#%s)",
            request.user, request.user.id, group.name, group.id
        )

    # Call the next function in chain
    return action(group, request)
```