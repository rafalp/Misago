# `delete_group_hook`

This hook wraps the standard function that Misago uses to delete a user group.

Misago executes delete queries for groups and their relations directly, skipping the Django ORM which uses the Object Collector logic to simulate the delete cascade behavior that databases implement and run the pre and post delete signals.

Because of this, plugins need to explicitly delete objects related to the deleted group in custom filters before a group itself is deleted from the database.


## Location

This hook can be imported from `misago.users.hooks`:

```python
from misago.users.hooks import delete_group_hook
```


## Filter

```python
def custom_delete_group_filter(
    action: DeleteGroupHookAction,
    group: Group,
    request: HttpRequest | None=None,
) -> None:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: DeleteGroupHookAction`

A standard Misago function used for deleting the user group, or the next filter function from another plugin.

See the [action](#action) section for details.


#### `group: Group`

A `Group` model instance to delete from the database.


#### `request: Optional[HttpRequest]`

The request object or `None` if it was not provided.


## Action

```python
def delete_group_action(group: Group, request: HttpRequest | None=None) -> None:
    ...
```

A standard Misago function used for deleting the user group, or the next filter function from another plugin.


### Arguments

#### `group: Group`

A `Group` model instance to delete from the database.


#### `request: Optional[HttpRequest]`

The request object or `None` if it was not provided.


## Example

The code below implements a custom filter function that deletes a custom model implemented in a plugin before group itself is deleted:

```python
from django.http import HttpRequest
from misago.postgres.delete import delete_all
from misago.users.models import Group

from .models import GroupPromotionRule

@delete_group_hook.append_filter
def delete_group_promotion_rules(
    action, group: Group, request: HttpRequest | None = None
) -> None:
    # Delete promotion rules related with this group bypassing the Django ORM
    delete_all(GroupPromotionRule, group_id=group.id)

    # Call the next function in chain
    return action(group, request)
```