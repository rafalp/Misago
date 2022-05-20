# `thread_open_hook`

```python
from misago.graphql.thread.hooks.threadopen import thread_open_hook

thread_open_hook.call_action(
    action: ThreadOpenAction,
    context: Context,
    cleaned_data: ThreadOpenInput,
)
```

A filter for the function used by `threadOpen` GraphQL mutation to update the thread in the database.

Returns `Thread` dataclass with updated thread data.


## Required arguments

### `action`

```python
async def open_thread(context: Context, cleaned_data: ThreadOpenInput) -> Thread:
    ...
```

Next filter or built-in function used to update the thread in the database.


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
class ThreadOpenInput(TypedDict):
    thread: Thread
```