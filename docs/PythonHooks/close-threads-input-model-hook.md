# `close_threads_input_model_hook`

```python
from misago.hooks.closethreads import close_threads_input_model_hook

close_threads_input_model_hook.call_action(
    action: CloseThreadsInputModelAction, context: GraphQLContext
)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `CloseThreadsInputModel` GraphQL input type used by the "close threads" GraphQL mutation.

Returns `CloseThreadsInputModel` input model type.


## Required arguments

### `action`

```python
async def create_input_model(context: GraphQLContext) -> CloseThreadsInputModel:
    ...
```

Next filter or built-in function used to create input model type.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.