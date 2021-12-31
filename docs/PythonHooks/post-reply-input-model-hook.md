# `post_reply_input_model_hook`

```python
from misago.graphql.public.mutations.hooks.postreply import post_reply_input_model_hook

post_reply_input_model_hook.call_action(
    action: PostReplyInputModelAction, context: GraphQLContext
)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `PostReplyInputModel` GraphQL input type used by the "post reply" GraphQL mutation.

Returns `PostReplyInputModel` input model type.


## Required arguments

### `action`

```python
async def create_input_model(context: GraphQLContext) -> PostReplyInputModel:
    ...
```

Next filter or built-in function used to create input model type.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.