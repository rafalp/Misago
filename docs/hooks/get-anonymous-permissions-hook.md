# `get_anonymous_permissions_hook`

```python
from misago.permissions.hooks import get_anonymous_permissions_hook

get_anonymous_permissions_hook.call_action(
    action: GetAnonymousPermissionsAction,
    context: Context,
)
```

A filter for the function used by Misago to retrieve anonymous (unauthenticated) user's permissions.

Returns dict with permissions.


## Required arguments

### `action`

```python
async def get_anonymous_permissions(
    context: Context,
) -> dict:
    ...
```

Next filter or built-in function used to retrieve anonymous (unauthenticated) user's permissions.


### `context`

```python
Context
```

A dict with GraphQL query context.
