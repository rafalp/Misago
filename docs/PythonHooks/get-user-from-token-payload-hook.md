# `get_user_from_token_payload_hook`

```python
get_user_from_token_payload_hook.call_action(
    action: GetUserFromTokenAction,
    context: GraphQLContext,
    payload: Dict[str, Any],
    in_admin: bool,
)
```

A filter for the function used to get user for given authorization token payload.

Returns `User` dataclass with authorized user data or `None` if token's payload was invalid or expired.


## Required arguments

### `action`

```python
async def get_user_from_token_payload(
    context: GraphQLContext, token_payload: Dict[str, any], in_admin: bool
) -> Optional[User]:
    ...
```

Next filter or built-in function used to obtain user for authorization token payload.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


## `payload`

```python
Dict[str, Any]
```

A `dict` containing payload extracted from authorization token.


### `in_admin`

```python
bool
```

`True` if user is being retrieved in the admin panel, `False` otherwise.