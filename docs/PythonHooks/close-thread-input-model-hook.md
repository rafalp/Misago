# `close_thread_input_model_hook`

```python
from misago.hooks.closethread import close_thread_input_model_hook

close_thread_input_model_hook.call_action(
    action: CloseThreadInputModelAction, context: GraphQLContext
)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `CloseThreadInputModel` GraphQL input type used by the "close thread" GraphQL mutation.

Returns `CloseThreadInputModel` input model type.


## Required arguments

### `action`

```python
async def create_input_model(context: GraphQLContext) -> CloseThreadInputModel:
    ...
```

Next filter or built-in function used to create input model type.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.