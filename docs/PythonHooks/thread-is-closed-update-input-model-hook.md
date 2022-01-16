# `thread_is_closed_update_input_model_hook`

```python
from misago.graphql.public.mutations.hooks.threadisclosedupdate import thread_is_closed_update_input_model_hook

thread_is_closed_update_input_model_hook.call_action(
    action: ThreadIsClosedUpdateInputModelAction, context: GraphQLContext
)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `ThreadIsClosedUpdateInputModel` GraphQL input type used by `threadIsClosedUpdate` GraphQL mutation.

Returns `ThreadIsClosedUpdateInputModel` input model type.


## Required arguments

### `action`

```python
async def create_input_model(context: GraphQLContext) -> ThreadIsClosedUpdateInputModel:
    ...
```

Next filter or built-in function used to create input model type.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.