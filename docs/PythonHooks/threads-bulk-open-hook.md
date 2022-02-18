# `threads_bulk_open_hook`

```python
from misago.graphql.public.mutations.hooks.threadsbulkopen import threads_bulk_open_hook

threads_bulk_open_hook.call_action(
    action: ThreadsBulkOpenAction,
    context: Context,
    cleaned_data: ThreadsBulkOpenInput,
)
```

A filter for the function used by `threadsBulkOpen` GraphQL mutation to update threads in the database.

Returns `list` of `Thread` dataclasses with updated threads data.


## Required arguments

### `action`

```python
async def open_threads(context: Context, cleaned_data: ThreadsBulkOpenInput) -> List[Thread]:
    ...
```

Next filter or built-in function used to update the threads in the database.


### `context`

```python
Context
```

A dict with GraphQL query context.


### `cleaned_data`

```python
Dict[str, Any]
```

A dict with already validated and cleaned input data:

```python
class ThreadsBulkOpenInput(TypedDict):
    threads: List[Thread]
```