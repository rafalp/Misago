# `thread_open_hook`

```python
from misago.graphql.public.mutations.hooks.threadopen import thread_open_hook

thread_open_hook.call_action(
    action: ThreadOpenAction,
    context: GraphQLContext,
    cleaned_data: ThreadOpenInput,
)
```

A filter for the function used by `threadOpen` GraphQL mutation to update the thread in the database.

Returns `Thread` dataclass with updated thread data.


## Required arguments

### `action`

```python
async def open_thread(context: GraphQLContext, cleaned_data: ThreadOpenInput) -> Thread:
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
class ThreadOpenInput(TypedDict):
    thread: Thread
```