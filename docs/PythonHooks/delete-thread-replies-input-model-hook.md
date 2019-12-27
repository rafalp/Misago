# `delete_thread_replies_input_model_hook`

```python
delete_thread_replies_input_model_hook.call_action(
    action: DeleteThreadRepliesInputModelAction, context: GraphQLContext
)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `DeleteThreadRepliesInputModel` GraphQL input type used by the "delete thread replies" GraphQL mutation.

Returns `DeleteThreadRepliesInputModel` input model type.


## Required arguments

### `action`

```python
async def create_input_model(context: GraphQLContext) -> DeleteThreadRepliesInputModel:
    ...
```

Next filter or built-in function used to create input model type.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.