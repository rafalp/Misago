# `edit_thread_title_input_model_hook`

```python
edit_thread_title_input_model_hook.call_action(action: EditThreadTitleInputModelAction, context: GraphQLContext)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `EditThreadTitleInputModel` GraphQL input type used by the "edit thread title" GraphQL mutation.

Returns `EditThreadTitleInputModel` input model type.


## Required arguments

### `action`

```python
async def create_input_model(context: GraphQLContext) -> EditThreadTitleInputModel:
    ...
```

Next filter or built-in function used to create input model type.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.