# `thread_delete_input_model_hook`

```python
from misago.graphql.public.mutations.hooks.threaddelete import thread_delete_input_model_hook

thread_delete_input_model_hook.call_action(
    action: ThreadDeleteInputModelAction, context: GraphQLContext
)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `ThreadDeleteInputModel` GraphQL input type used by `threadDelete` GraphQL mutation.

Returns `ThreadDeleteInputModel` input model type.


## Required arguments

### `action`

```python
async def create_input_model(context: GraphQLContext) -> ThreadDeleteInputModel:
    ...
```

Next filter or built-in function used to create input model type.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.