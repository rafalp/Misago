# `user_create_hook`

```python
from misago.graphql.public.mutations.hooks.usercreate import user_create_hook

user_create_hook.call_action(
    action: UserCreateAction,
    context: Context,
    cleaned_data: UserCreateInput
)
```

A filter for the function used by `userCreate` GraphQL mutation to register new user account in the database.

Returns `User` dataclass with newly created user data.


## Required arguments

### `action`

```python
async def register_user(context: Context, cleaned_data: UserCreateInput) -> User:
    ...
```

Next filter or built-in function used to register new user account in the database.


### `context`

```python
Context
```

A dict with GraphQL query context.


### `cleaned_data`

```python
Dict[str, Any]
```

A dict with already validated and cleaned input data. Will contain at least `name`, `email` and `password` keys, all being strings.

Plugins may add additional `captcha` key to this data.