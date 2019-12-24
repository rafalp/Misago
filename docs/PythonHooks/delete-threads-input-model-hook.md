# `delete_threads_input_model_hook`

```python
delete_threads_input_model_hook.call_action(action: DeleteThreadsInputModelAction, context: GraphQLContext)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `DeleteThreadsInputModel` GraphQL input type used by the "delete threads" GraphQL mutation.

Returns `DeleteThreadsInputModel` input model type.


## Required arguments

### `action`

```python
async def create_input_model(context: GraphQLContext) -> DeleteThreadsInputModel:
    ...
```

Next filter or built-in function used to create input model type.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.