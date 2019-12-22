# `post_thread_input_model_hook`

```python
post_thread_input_model_hook.call_action(action: PostThreadInputModelAction, context: GraphQLContext)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `PostThreadInputModel` GraphQL input type used by the "post thread" GraphQL mutation.

Returns `PostThreadInputModel` input model type.


## Required arguments

### `action`

```python
async def create_input_model(context: GraphQLContext) -> PostThreadInputModel:
    ...
```

Next filter or built-in function used to create input model type.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.