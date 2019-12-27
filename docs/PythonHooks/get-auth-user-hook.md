# `get_auth_user_hook`

```python
get_auth_user_hook.call_action(
    action: GetAuthUserAction, context: GraphQLContext, user_id: int
)
```

A filter for the function used to get authorized user for given auth credential (eg. token).

Returns `User` dataclass with authorized user data or `None` if user was not found or couldn't be authenticated for other reason (eg. deactivated).


## Required arguments

### `action`

```python
async def get_user(context: GraphQLContext, user_id: int) -> Optional[User]:
    ...
```

Next filter or built-in function used to obtain authorized user by their id.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


## `user_id`

```python
int
```

An `int` containing authorized user's id. May no longer exist in database.