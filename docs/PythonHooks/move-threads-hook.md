# `move_threads_hook`

```python
from misago.graphql.public.mutations.hooks.movethreads import move_threads_hook

move_threads_hook.call_action(
    action: MoveThreadsAction,
    context: GraphQLContext,
    cleaned_data: MoveThreadsInput,
)
```

A filter for the function used by GraphQL mutation moving threads to update threads and their posts in the database.

Returns list of `Thread` dataclasses with updated threads data.


## Required arguments

### `action`

```python
async def move_threads(context: GraphQLContext, cleaned_data: MoveThreadsInput) -> List[Thread]:
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
class MoveThreadsInput(TypedDict):
    threads: List[Thread]
    category: Category
```