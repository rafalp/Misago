# `thread_category_update_input_model_hook`

```python
from misago.graphql.public.mutations.hooks.threadcategoryupdate import thread_category_update_input_model_hook

thread_category_update_input_model_hook.call_action(
    action: ThreadCategoryUpdateInputModelAction,
    context: GraphQLContext,
)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `ThreadCategoryUpdateInputModel` GraphQL input type used by the `threadCategoryUpdate` GraphQL mutation.

Returns `ThreadCategoryUpdateInputModel` input model type.


## Required arguments

### `action`

```python
async def create_input_model(context: GraphQLContext) -> ThreadCategoryUpdateInputModel:
    ...
```

Next filter or built-in function used to create input model type.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.