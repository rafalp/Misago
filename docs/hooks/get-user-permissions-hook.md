# `get_user_permissions_hook`

```python
from misago.permissions.hooks import get_user_permissions_hook

get_user_permissions_hook.call_action(
    action: GetUserPermissionsAction,
    context: Context,
    user: User,
)
```

A filter for the function used by Misago to retrieve user's permissions.

Returns dict with user permissions.


## Required arguments

### `action`

```python
async def get_user_permissions(
    context: Context,
    user: User,
) -> dict:
    ...
```

Next filter or built-in function used to retrieve user's permissions.


### `context`

```python
Context
```

A dict with GraphQL query context.


### `user`

```python
User
```

`User` dataclass representing user whose permissions should be retrieved.
