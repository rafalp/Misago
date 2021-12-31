# `close_threads_hook`

```python
from misago.graphql.public.mutations.hooks.closethreads import close_threads_hook

close_threads_hook.call_action(
    action: CloseThreadsAction,
    context: GraphQLContext,
    cleaned_data: CloseThreadsInput,
)
```

A filter for the function used by GraphQL mutation closing threads to update threads in the database.

Returns `list` of `Thread` dataclasses with updated threads data.


## Required arguments

### `action`

```python
async def close_threads(context: GraphQLContext, cleaned_data: CloseThreadsInput) -> List[Thread]:
    ...
```

Next filter or built-in function used to update the threads in the database.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


### `cleaned_data`

```python
Dict[str, Any]
```

A dict with already validated and cleaned input data. Will contain at least `threads` and `is_closed` keys:

```python
class CloseThreadsInput(TypedDict):
    threads: List[Thread]
    is_closed: bool
```