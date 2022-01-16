# `post_create_input_model_hook`

```python
from misago.graphql.public.mutations.hooks.postcreate import post_create_input_model_hook

post_create_input_model_hook.call_action(
    action: PostCreateInputModelAction, context: GraphQLContext
)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `PostCreateInputModel` GraphQL input type used by the `postCreate` GraphQL mutation.

Returns `PostCreateInputModel` input model type.


## Required arguments

### `action`

```python
async def create_input_model(context: GraphQLContext) -> PostCreateInputModel:
    ...
```

Next filter or built-in function used to create input model type.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.