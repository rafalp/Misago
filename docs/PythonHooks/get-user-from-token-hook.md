# `get_user_from_token_hook`

```python
from misago.hooks.auth import get_user_from_token_hook

get_user_from_token_hook.call_action(
    action: GetUserFromTokenAction, context: GraphQLContext, token: str, in_admin: bool
)
```

A filter for the function used to get user for given authorization token.

Returns `User` dataclass with authorized user data or `None` if token was invalid or expired.


## Required arguments

### `action`

```python
async def get_user_from_token(
    context: GraphQLContext, token: str, in_admin: bool
) -> Optional[User]:
    ...
```

Next filter or built-in function used to obtain user for authorization token.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


## `token`

```python
str
```

A `str` containing authorization token. It may be invalid.


### `in_admin`

```python
bool
```

`True` if user is being retrieved in the admin panel, `False` otherwise.