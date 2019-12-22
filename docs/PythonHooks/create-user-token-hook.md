# `create_user_token_hook`

```python
create_user_token_hook.call_action(action: CreateUserTokenAction, context: GraphQLContext, user: User)
```

A filter for the function used to create an authorization token for user.

Returns `str` with authorization token that should be included by the client in `Authorization` header in future calls to the API.


## Required arguments

### `action`

```python
async def create_user_token(context: GraphQLContext, user: User) -> str:
    ...
```

Next filter or built-in function used to create authorization token for user.


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