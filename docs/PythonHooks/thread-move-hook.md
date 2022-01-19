# `thread_move_hook`

```python
from misago.graphql.public.mutations.hooks.threadmove import thread_move_hook

thread_move_hook.call_action(
    action: ThreaddMoveAction,
    context: GraphQLContext,
    cleaned_data: dict,
)
```

A filter for the function used by `threadMove` GraphQL mutation to update the thread and its posts in the database.

Returns `Thread` dataclass with updated thread data.


## Required arguments

### `action`

```python
async def thread_move(context: GraphQLContext, cleaned_data: dict) -> Thread:
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
class ThreadMoveInput(TypedDict):
    thread: Thread
    category: Category
```

A dict with already validated and cleaned input data.