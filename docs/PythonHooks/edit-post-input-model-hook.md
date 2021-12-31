# `edit_post_input_model_hook`

```python
from misago.graphql.public.mutations.hooks.editpost import edit_post_input_model_hook

edit_post_input_model_hook.call_action(
    action: EditPostInputModelAction, context: GraphQLContext
)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `EditPostInputModel` GraphQL input type used by the "post reply" GraphQL mutation.

Returns `EditPostInputModel` input model type.


## Required arguments

### `action`

```python
async def create_input_model(context: GraphQLContext) -> EditPostInputModel:
    ...
```

Next filter or built-in function used to create input model type.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.