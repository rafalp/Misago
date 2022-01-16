# `post_update_input_model_hook`

```python
from misago.graphql.public.mutations.hooks.postupdate import post_update_input_model_hook

post_update_input_model_hook.call_action(
    action: PostUpdateInputModelAction, context: GraphQLContext
)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `PostUpdateInputModel` GraphQL input type used by the `postUpdate` GraphQL mutation.

Returns `PostUpdateInputModel` input model type.


## Required arguments

### `action`

```python
async def create_input_model(context: GraphQLContext) -> PostUpdateInputModel:
    ...
```

Next filter or built-in function used to create input model type.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.