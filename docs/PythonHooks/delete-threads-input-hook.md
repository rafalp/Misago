# `delete_threads_input_hook`

```python
delete_threads_input_hook.call_action(
    action: DeleteThreadsInputAction,
    context: GraphQLContext,
    validators: Dict[str, List[AsyncValidator]],
    data: DeleteThreadsInput,
    errors_list: ErrorsList,
)
```

A filter for the function used to validate data for `DeleteThreadsInputModel` GraphQL input type.

Returns a tuple of `data` that should be used to delete threads and validation `errors`.


## Required arguments

### `action`

```python
async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[AsyncValidator]],
    data: DeleteThreadsInput,
    errors: ErrorsList,
) -> Tuple[DeleteThreadsInput, ErrorsList]:
    ...
```

Next filter or built-in function used to validate deleted threads input data.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


### `validators`

```python
Dict[str, List[AsyncValidator]]
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