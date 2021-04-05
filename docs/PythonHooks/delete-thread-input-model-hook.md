# `misago.hooks.deletethread.delete_thread_input_model_hook`

```python
delete_thread_input_model_hook.call_action(
    action: DeleteThreadInputModelAction, context: GraphQLContext
)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `DeleteThreadInputModel` GraphQL input type used by the "delete thread" GraphQL mutation.

Returns `DeleteThreadInputModel` input model type.


## Required arguments

### `action`

```python
async def create_input_model(context: GraphQLContext) -> DeleteThreadInputModel:
    ...
```

Next filter or built-in function used to create input model type.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.