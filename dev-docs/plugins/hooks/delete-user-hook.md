# `delete_user_hook`

This hook wraps the Misago function used to delete a user.

 # Example

The code below implements a custom filter function that logs delete.

 ```python import logging from typing import list, Protocol

from django.contrib.auth import get_user_model from django.http import HttpRequest from misago.enums import DeleteUserContentAction from misago.users.hooks import delete_user_hook

User = get_user_model()

logger = logging.getLogger("user.delete")

@delete_user_hook.append_filter def log_delete_user(     action,     user: User,     content_action: DeleteUserContentAction,     *,     context: dict[str, Any] | None = None, ):     action(         user,         content_action=content_action,         context=context,     )

    logger.info(         "Deleted users: %s", user.username,         extra={"user": user},     )```


## Location

This hook can be imported from `misago.users.hooks`:

```python
from misago.users.hooks import delete_user_hook
```


## Filter

```python
def custom_delete_user_filter(
    action: DeleteUserHookAction,
    user: User,
    content_action: DeleteUserContentAction,
    *,
    context: dict[str, Any] | None=None,
):
    ...
```

A function implemented by a plugin that can be registered in this hook.


### Arguments:

#### `action: DeleteUserHookAction`

Next function registered in this hook, either a custom function or Misago's standard one.

See the [action](#action) section for details.


#### `user: User`

User instance that will be deleted.


#### `content_action: DeleteUserContentAction`

Action determining what happens to user's content.


#### `context: dict[str, Any] | None`

Additional context passed to the deletion action.


## Action

```python
def delete_user_action(
    user: User,
    content_action: DeleteUserContentAction,
    *,
    context: dict[str, Any] | None=None,
):
    ...
```

Misago function used to delete a user.


### Arguments:

#### `user: User`

User instance that will be deleted.


#### `content_action: DeleteUserContentAction`

Action determining what happens to user's content.


#### `context: dict[str, Any] | None`

Additional context passed to the deletion action.