# `create_user_token_payload_hook`

```python
from misago.hooks.auth import create_user_token_payload_hook

create_user_token_payload_hook.call_action(
    action: CreateUserTokenPayloadAction,
    context: GraphQLContext,
    user: User,
    in_admin: bool
)
```

A filter for the function used to create an payload for user authorization token.

Returns `dict` which should be used as JWT token's payload.


## Required arguments

### `action`

```python
async def create_user_token_payload(
    context: GraphQLContext, user: User, in_admin: bool
) -> Dict[str, Any]:
    ...
```

Next filter or built-in function used to create payload for user authorization token.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


## `user`

```python
User
```

A `dict` containing authorized user's data.


### `in_admin`

```python
bool
```

`True` if token payload will be used by the admin panel, `False` otherwise.