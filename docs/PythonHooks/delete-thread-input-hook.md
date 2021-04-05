# `misago.hooks.deletethread.delete_thread_input_hook`

```python
delete_thread_input_hook.call_action(
    action: DeleteThreadInputAction,
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: DeleteThreadInput,
    errors_list: ErrorsList,
)
```

A filter for the function used to validate data for `DeleteThreadInputModel` GraphQL input type.

Returns a tuple of `data` that should be used to delete the thread and validation `errors`.


## Required arguments

### `action`

```python
async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: DeleteThreadInput,
    errors: ErrorsList,
) -> Tuple[DeleteThreadInput, ErrorsList]:
    ...
```

Next filter or built-in function used to validate input data.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


### `validators`

```python
Dict[str, List[Validator]]
```

A dict of lists of validators that should be used to validate inputs values.


### `data`

```python
Dict[str, Any]
```

A dict with input data that passed initial cleaning and validation. If any of fields failed initial cleanup and validation, it won't be present in this dict.


### `errors`

```python
ErrorsList
```

List of validation errors found so far. Can be extended using it's `add_error` and `add_root_error` methods.