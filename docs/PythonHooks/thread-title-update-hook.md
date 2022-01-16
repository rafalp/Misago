# `thread_title_update_hook`

```python
from misago.graphql.public.mutations.hooks.threadtitleupdate import thread_title_update_hook

thread_title_update_hook.call_action(
    action: ThreadTitleUpdateAction,
    context: GraphQLContext,
    cleaned_data: ThreadTitleUpdateInput,
)
```

A filter for the function used by `threadTitleUpdate` GraphQL mutation to update the thread in the database.

Returns `Thread` dataclass with updated thread data.


## Required arguments

### `action`

```python
async def thread_title_update(context: GraphQLContext, cleaned_data: ThreadTitleUpdateInput) -> Thread:
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

A dict with already validated and cleaned input data. Will contain at least `thread` and `title` keys:

```python
class ThreadTitleUpdateInput(TypedDict):
    thread: Thread
    title: str
```