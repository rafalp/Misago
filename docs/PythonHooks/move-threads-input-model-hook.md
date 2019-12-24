# `move_threads_input_model_hook`

```python
move_threads_input_model_hook.call_action(action: MoveThreadsInputModelAction, context: GraphQLContext)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `MoveThreadsInputModel` GraphQL input type used by the "move threads" GraphQL mutation.

Returns `MoveThreadsInputModel` input model type.


## Required arguments

### `action`

```python
async def create_input_model(context: GraphQLContext) -> MoveThreadsInputModel:
    ...
```

Next filter or built-in function used to create input model type.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.