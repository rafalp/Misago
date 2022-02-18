# `threads_bulk_delete_hook`

```python
from misago.graphql.public.mutations.hooks.threadsbulkdelete import threads_bulk_delete_hook

threads_bulk_delete_hook.call_action(
    action: ThreadsBulkDeleteAction,
    context: Context,
    cleaned_data: ThreadsBulkDeleteInput,
)
```

A filter for the function used by `threadsBulkDelete` GraphQL to delete threads and their posts from the database.

Returns `None`.


## Required arguments

### `action`

```python
async def delete_threads(context: Context, cleaned_data: ThreadsBulkDeleteInput):
    ...
```

Next filter or built-in function used to delete threads from the database.


### `context`

```python
Context
```

A dict with GraphQL query context.


### `cleaned_data`

```python
Dict[str, Any]
```

A dict with already validated and cleaned input data. Will contain `threads` key:

```python
class ThreadsBulkDeleteInput(TypedDict):
    threads: List[Thread]
```