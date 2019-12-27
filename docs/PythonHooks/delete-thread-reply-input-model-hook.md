# `delete_thread_reply_input_model_hook`

```python
delete_thread_reply_input_model_hook.call_action(
    action: DeleteThreadReplyInputModelAction, context: GraphQLContext
)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `DeleteThreadReplyInputModel` GraphQL input type used by the "delete thread reply" GraphQL mutation.

Returns `DeleteThreadReplyInputModel` input model type.


## Required arguments

### `action`

```python
async def create_input_model(context: GraphQLContext) -> DeleteThreadReplyInputModel:
    ...
```

Next filter or built-in function used to create input model type.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.