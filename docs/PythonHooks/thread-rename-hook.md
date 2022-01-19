# `thread_rename_hook`

```python
from misago.graphql.public.mutations.hooks.threadrename import thread_rename_hook

thread_rename_hook.call_action(
    action: ThreadRenameAction,
    context: GraphQLContext,
    cleaned_data: ThreadRenameInput,
)
```

A filter for the function used by `threadRename` GraphQL mutation to update the thread in the database.

Returns `Thread` dataclass with updated thread data.


## Required arguments

### `action`

```python
async def thread_rename(context: GraphQLContext, cleaned_data: ThreadRenameInput) -> Thread:
    ...
```

Next filter or built-in function used to update the thread in the database.


### `context`

```python
GraphQLContext
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