# `register_user_hook`

```python
from misago.graphql.public.mutations.hooks.registeruser import register_user_hook

register_user_hook.call_action(
    action: RegisterUserAction,
    context: GraphQLContext,
    cleaned_data: RegisterUserInput
)
```

A filter for the function used by GraphQL mutation registering new user account to register new user in the database.

Returns `User` dataclass with newly created user data.


## Required arguments

### `action`

```python
async def register_user(context: GraphQLContext, cleaned_data: RegisterUserInput) -> User:
    ...
```

Next filter or built-in function used to register new user account in the database.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


### `cleaned_data`

```python
Dict[str, Any]
```

A dict with already validated and cleaned input data. Will contain at least `name`, `email` and `password` keys, all being strings.