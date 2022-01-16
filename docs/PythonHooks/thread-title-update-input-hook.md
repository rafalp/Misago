# `thread_title_update_input_hook`

```python
from misago.graphql.public.mutations.hooks.threadtitleupdate import thread_title_update_input_hook

thread_title_update_input_hook.call_action(
    action: ThreadTitleUpdateInputAction,
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: ThreadTitleUpdateInput,
    errors_list: ErrorsList,
)
```

A filter for the function used to validate data for `ThreadTitleUpdateInputModel` GraphQL input type used by `threadTitleUpdate` GraphQL mutation.

Returns a tuple of `data` that should be used to update the thread and validation `errors`.


## Required arguments

### `action`

```python
async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[Validator]],
    data: ThreadTitleUpdateInput,
    errors: ErrorsList,
) -> Tuple[ThreadTitleUpdateInput, ErrorsList]:
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