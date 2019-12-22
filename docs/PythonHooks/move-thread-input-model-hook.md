# `move_thread_input_model_hook`

```python
move_thread_input_model_hook.call_action(action: MoveThreadInputModelAction, context: GraphQLContext)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `MoveThreadInputModel` GraphQL input type used by the "move thread" GraphQL mutation.

Returns `MoveThreadInputModel` input model type.


## Required arguments

### `action`

```python
async def create_input_model(context: GraphQLContext) -> MoveThreadInputModel:
    ...
```

Next filter or built-in function used to create input model type.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.