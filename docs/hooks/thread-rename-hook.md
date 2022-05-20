# `thread_rename_hook`

```python
from misago.graphql.thread.hooks.threadrename import thread_rename_hook

thread_rename_hook.call_action(
    action: ThreadRenameAction,
    context: Context,
    cleaned_data: ThreadRenameInput,
)
```

A filter for the function used by `threadRename` GraphQL mutation to update the thread in the database.

Returns `Thread` dataclass with updated thread data.


## Required arguments

### `action`

```python
async def thread_rename(context: Context, cleaned_data: ThreadRenameInput) -> Thread:
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
class ThreadRenameInput(TypedDict):
    thread: Thread
    title: str
```