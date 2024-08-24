# `get_thread_posts_feed_users_hook`

This hook wraps the standard function that Misago uses to get a `dict` of `User` instances used to display thread posts feed. Users have their `group` field already populated.


## Location

This hook can be imported from `misago.threads.hooks`:

```python
from misago.threads.hooks import get_thread_posts_feed_users_hook
```


## Filter

```python
def custom_get_thread_posts_feed_users_filter(
    action: GetThreadPostsFeedUsersHookAction,
    request: HttpRequest,
    user_ids: set[int],
) -> dict[int, 'User']:
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments

#### `action: GetThreadPostsFeedUsersHookAction`

A standard Misago function used to get a `dict` of `User` instances used to display thread posts feed. Users have their `group` field populated.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `user_ids: set[int]`

A set of IDs of `User` objects to retrieve from the database


#### Return value

A `dict` of `User` instances, indexed by their IDs.


## Action

```python
def get_thread_posts_feed_users_action(request: HttpRequest, user_ids: set[int]) -> dict[int, 'User']:
    ...
```

A standard Misago function used to get a `dict` of `User` instances used to display thread posts feed. Users have their `group` field already populated.


### Arguments

#### `request: HttpRequest`

The request object.


#### `user_ids: set[int]`

A set of IDs of `User` objects to retrieve from the database


#### Return value

A `dict` of `User` instances, indexed by their IDs.


## Example

The code below implements a custom filter function that removes some users from the dictionary, making them display on a posts feed as deleted users.

```python
from typing import TYPE_CHECKING

from django.http import HttpRequest
from misago.threads.hooks import get_thread_posts_feed_users_hook

if TYPE_CHECKING:
    from misago.users.models import User


@get_thread_posts_feed_users_hook.append_filter
def replace_post_poster(
    action, request: HttpRequest, user_ids: set[int]
) -> dict[int, "User"]:
    users = action(request, user_ids)

    for user_id, user in list(users.items())
        if user.plugin_data.get("is_hidden"):
            del users[user_id]

    return users
```