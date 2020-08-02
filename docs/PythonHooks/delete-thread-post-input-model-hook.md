# `delete_thread_post_input_model_hook`

```python
delete_thread_post_input_model_hook.call_action(
    action: DeleteThreadPostInputModelAction, context: GraphQLContext
)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `DeleteThreadPostInputModel` GraphQL input type used by the "delete thread post" GraphQL mutation.

Returns `DeleteThreadPostInputModel` input model type.


## Required arguments

### `action`

```python
async def create_input_model(context: GraphQLContext) -> DeleteThreadPostInputModel:
    ...
```

Next filter or built-in function used to create input model type.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.