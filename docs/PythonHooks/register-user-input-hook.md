# `register_user_input_hook`

```python
register_user_input_hook.call_action(
    action: RegisterUserInputAction,
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: RegisterUserInput,
    errors_list: ErrorsList
)
```

A filter for the function used to validate data for `RegisterUserInputModel` GraphQL input type.

Returns a tuple of `data` that should be used to create new user and validation `errors`.


## Required arguments

### `action`

```python
async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: RegisterUserInput,
    errors: ErrorsList,
) -> Tuple[RegisterUserInput, ErrorsList]:
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