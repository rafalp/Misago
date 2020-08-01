# `delete_thread_posts_input_model_hook`

```python
delete_thread_posts_input_model_hook.call_action(
    action: DeleteThreadPostsInputModelAction, context: GraphQLContext
)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `DeleteThreadPostsInputModel` GraphQL input type used by the "delete thread posts" GraphQL mutation.

Returns `DeleteThreadPostsInputModel` input model type.


## Required arguments

### `action`

```python
async def create_input_model(context: GraphQLContext) -> DeleteThreadPostsInputModel:
    ...
```

Next filter or built-in function used to create input model type.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.