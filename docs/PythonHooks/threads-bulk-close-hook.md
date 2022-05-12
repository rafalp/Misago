# `threads_bulk_close_hook`

```python
from misago.graphql.thread.hooks.threadsbulkclose import threads_bulk_close_hook

threads_bulk_close_hook.call_action(
    action: ThreadsBulkCloseAction,
    context: Context,
    cleaned_data: ThreadsBulkCloseInput,
)
```

A filter for the function used by `threadsBulkClose` GraphQL mutation to update threads in the database.

Returns `list` of `Thread` dataclasses with updated threads data.


## Required arguments

### `action`

```python
async def close_threads(context: Context, cleaned_data: ThreadsBulkCloseInput) -> List[Thread]:
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
class ThreadsBulkCloseInput(TypedDict):
    threads: List[Thread]
```