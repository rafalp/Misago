# `get_user_from_context_hook`


```python
get_user_from_token_hook.get_user_from_context_hook(action: GetUserFromContextAction, context: GraphQLContext)
```

A filter for the function used to get user for current context.

Returns `User` dataclass with authorized user data or `None` if context didn't contain data required to resolve authorized user.


## Required arguments

### `action`

```python
async def get_user_from_context(context: GraphQLContext) -> Optional[User]:
    ...
```

Next filter or built-in function used to obtain user for current context.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.