# `thread_is_closed_update_hook`

```python
from misago.graphql.public.mutations.hooks.threadisclosedupdate import thread_is_closed_update_hook

thread_is_closed_update_hook.call_action(
    action: ThreadIsClosedUpdateAction,
    context: GraphQLContext,
    cleaned_data: ThreadIsClosedUpdateInput,
)
```

A filter for the function used by `threadIsClosedUpdate` GraphQL mutation to update the thread in the database.

Returns `Thread` dataclass with updated thread data.


## Required arguments

### `action`

```python
async def close_thread(context: GraphQLContext, cleaned_data: ThreadIsClosedUpdateInput) -> Thread:
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

A dict with already validated and cleaned input data. Will contain at least `thread` and `is_closed` keys:

```python
class ThreadIsClosedUpdateInput(TypedDict):
    thread: Thread
    is_closed: bool
```