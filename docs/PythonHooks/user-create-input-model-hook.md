# `user_create_input_model_hook`

```python
from misago.graphql.public.mutations.hooks.usercreate import user_create_input_model_hook

user_create_input_model_hook.call_action(
    action: UserCreateInputModelAction,
    context: Context,
)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `UserCreateInputModel` GraphQL input type used by `userCreate` GraphQL mutation.

Returns `UserCreateInputModel` input model type.


## Required arguments

### `action`

```python
async def create_input_model(context: Context) -> UserCreateInputModel:
    ...
```

Next filter or built-in function used to create input model type.


### `context`

```python
Context
```

A dict with GraphQL query context.