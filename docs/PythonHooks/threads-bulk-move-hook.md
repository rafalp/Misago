# `threads_bulk_move_hook`

```python
from misago.graphql.public.mutations.hooks.threadsbulkmove import threads_bulk_move_hook

threads_bulk_move_hook.call_action(
    action: ThreadsBulkMoveAction,
    context: GraphQLContext,
    cleaned_data: ThreadsBulkMoveInput,
)
```

A filter for the function used by GraphQL `threadsBulkMove` mutation to update threads and their posts in the database.

Returns list of `Thread` dataclasses with updated threads data.


## Required arguments

### `action`

```python
async def move_threads(context: GraphQLContext, cleaned_data: ThreadsBulkMoveInput) -> List[Thread]:
    ...
```

Next filter or built-in function used to update threads in the database.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


### `cleaned_data`

```python
Dict[str, Any]
```

A dict with already validated and cleaned input data. Will contain at least `threads` and `category` keys:

```python
class ThreadsBulkMoveInput(TypedDict):
    threads: List[Thread]
    category: Category
```