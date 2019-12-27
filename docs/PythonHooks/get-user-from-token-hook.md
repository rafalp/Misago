# `get_user_from_token_hook`

```python
get_user_from_token_hook.call_action(
    action: GetUserFromTokenAction, context: GraphQLContext, token: str
)
```

A filter for the function used to get user for given authorization token.

Returns `User` dataclass with authorized user data or `None` if token was invalid or expired.


## Required arguments

### `action`

```python
async def get_user_from_token(context: GraphQLContext, token: str) -> Optional[User]:
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