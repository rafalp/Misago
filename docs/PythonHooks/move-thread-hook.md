# `move_thread_hook`

```python
move_thread_hook.call_action(
    action: MoveThreadAction,
    context: GraphQLContext,
    cleaned_data: MoveThreadInput,
)
```

A filter for the function used by GraphQL mutation moving thread to update the thread and its posts in the database.

Returns `Thread` dataclass with updated thread data.


## Required arguments

### `action`

```python
async def move_thread(context: GraphQLContext, cleaned_data: MoveThreadInput) -> Thread:
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

A dict with already validated and cleaned input data. Will contain at least `thread` and `category` keys:

```python
class MoveThreadInput(TypedDict):
    thread: Thread
    category: Category
```