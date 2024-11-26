# `set_posts_feed_item_users_hook`

This hook wraps the standard function that Misago uses to set `User` instances on a `dict` with thread posts feed item's data.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import set_posts_feed_item_users_hook
```


## Filter

```python
def custom_set_posts_feed_item_users_filter(
    action: SetPostFeedItemUsersHookAction,
    users: dict[int, 'User'],
    item: dict,
):
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: SetPostFeedItemUsersHookAction`

A standard Misago function used to set `User` instances on a `dict` with thread posts feed item's data.

See the [action](#action) section for details.


#### `users: dict[int, "User"]`

A `dict` of `User` instances, indexed by their IDs.


#### `item: dict`

A `dict` with posts feed item's data. Hook should update it using the `User` instances from the `users`.


## Action

```python
def set_posts_feed_item_users_action(users: dict[int, 'User'], item: dict):
    ...
```

A standard Misago function used to set `User` instances on a `dict` with thread posts feed item's data.


### Arguments

#### `users: dict[int, "User"]`

A `dict` of `User` instances, indexed by their IDs.


#### `item: dict`

A `dict` with posts feed item's data. Hook should update it using the `User` instances from the `users`.


## Example

The code below implements a custom filter function that replaces post's real author with other one:

```python
from typing import TYPE_CHECKING

from misago.threads.hooks import set_posts_feed_item_users_hook

if TYPE_CHECKING:
    from misago.users.models import User


@set_posts_feed_item_users_hook.append_filter
def replace_post_poster(
    action, users: dict[int, "User"], item: dict
):
    action(users, item)

    if item["type"] == "post":
        if override_poster := item["post"].plugin_data.get("poster_id"):
            item["poster"] = users[override_poster]
```