# `thread_close_hook`

```python
from misago.graphql.public.mutations.hooks.threadclose import thread_close_hook

thread_close_hook.call_action(
    action: ThreadCloseAction,
    context: GraphQLContext,
    cleaned_data: ThreadCloseInput,
)
```

A filter for the function used by `threadClose` GraphQL mutation to update the thread in the database.

Returns `Thread` dataclass with updated thread data.


## Required arguments

### `action`

```python
async def close_thread(context: GraphQLContext, cleaned_data: ThreadCloseInput) -> Thread:
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
class ThreadCloseInput(TypedDict):
    thread: Thread
```