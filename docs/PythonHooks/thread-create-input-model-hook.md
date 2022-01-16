# `thread_create_input_model_hook`

```python
from misago.graphql.public.mutations.hooks.threadcreate import thread_create_input_model_hook

thread_create_input_model_hook.call_action(
    action: ThreadCreateInputModelAction, context: GraphQLContext
)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `ThreadCreateInputModel` GraphQL input type used by the `threadCreate` GraphQL mutation.

Returns `ThreadCreateInputModel` input model type.


## Required arguments

### `action`

```python
async def create_input_model(context: GraphQLContext) -> ThreadCreateInputModel:
    ...
```

Next filter or built-in function used to create input model type.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.