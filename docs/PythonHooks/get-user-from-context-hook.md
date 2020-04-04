# `get_user_from_context_hook`


```python
get_user_from_context_hook.call_action(
    action: GetUserFromContextAction, context: GraphQLContext, in_admin: bool
)
```

A filter for the function used to get user for current context.

Returns `User` dataclass with authorized user data or `None` if context didn't contain data required to resolve authorized user.


## Required arguments

### `action`

```python
async def get_user_from_context(context: GraphQLContext, in_admin: bool) -> Optional[User]:
    ...
```

Next filter or built-in function used to obtain user for current context.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


### `in_admin`

```python
bool
```

`True` if user is being retrieved in the admin panel, `False` otherwise.