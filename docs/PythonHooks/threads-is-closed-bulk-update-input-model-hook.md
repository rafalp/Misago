# `threads_is_closed_bulk_update_input_model_hook`

```python
from misago.graphql.public.mutations.hooks.threadsisclosedbulkupdate import threads_is_closed_bulk_update_input_model_hook

threads_is_closed_bulk_update_input_model_hook.call_action(
    action: ThreadsIsClosedBulkUpdateInputModelAction, context: GraphQLContext
)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `ThreadsIsClosedBulkUpdateInputModel` GraphQL input type used by `threadsIsClosedBulkUpdate` GraphQL mutation.

Returns `ThreadsIsClosedBulkUpdateInputModel` input model type.


## Required arguments

### `action`

```python
async def create_input_model(context: GraphQLContext) -> ThreadsIsClosedBulkUpdateInputModel:
    ...
```

Next filter or built-in function used to create input model type.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.