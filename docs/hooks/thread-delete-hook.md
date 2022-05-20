# `thread_delete_hook`

```python
from misago.graphql.thread.hooks.threaddelete import thread_delete_hook

thread_delete_hook.call_action(
    action: ThreadDeleteAction,
    context: Context,
    cleaned_data: ThreadDeleteInput,
)
```

A filter for the function used by `threadDelete` GraphQL mutation to delete the thread and its posts from the database.

Returns `None`.


## Required arguments

### `action`

```python
async def thread_delete(context: Context, cleaned_data: ThreadDeleteInput):
    ...
```

Next filter or built-in function used to delete the thread from the database.


### `context`

```python
Context
```

A dict with GraphQL query context.


### `cleaned_data`

```python
Dict[str, Any]
```

A dict with already validated and cleaned input data. Will contain `thread` key:

```python
class ThreadDeleteInput(TypedDict):
    thread: Thread
```