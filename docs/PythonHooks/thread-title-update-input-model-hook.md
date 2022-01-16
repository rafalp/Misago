# `thread_title_update_input_model_hook`

```python
from misago.graphql.public.mutations.hooks.threadtitleupdate import thread_title_update_input_model_hook

thread_title_update_input_model_hook.call_action(
    action: ThreadTitleUpdateInputModelAction, context: GraphQLContext
)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `ThreadTitleUpdateInputModel` GraphQL input type used by the `threadTitleUpdate` GraphQL mutation.

Returns `ThreadTitleUpdateInputModel` input model type.


## Required arguments

### `action`

```python
async def create_input_model(context: GraphQLContext) -> ThreadTitleUpdateInputModel:
    ...
```

Next filter or built-in function used to create input model type.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.