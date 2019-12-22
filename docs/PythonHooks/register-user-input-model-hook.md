# `register_user_input_model_hook`

```python
register_user_input_model_hook.call_action(action: RegisterUserInputModelAction, context: GraphQLContext)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `RegisterUserInputModel` GraphQL input type used by the "register new user" GraphQL mutation.

Returns `RegisterUserInputModel` input model type.


## Required arguments

### `action`

```python
async def create_input_model(context: GraphQLContext) -> RegisterUserInputModel:
    ...
```

Next filter or built-in function used to create input model type.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.