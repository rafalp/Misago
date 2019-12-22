# `close_thread_hook`

```python
close_thread_hook.call_action(
    action: CloseThreadAction,
    context: GraphQLContext,
    cleaned_data: CloseThreadInput,
)
```

A filter for the function used by GraphQL mutation closing thread to update the thread in the database.

Returns `Thread` dataclass with updated thread data.


## Required arguments

### `action`

```python
async def close_thread(context: GraphQLContext, cleaned_data: CloseThreadInput) -> Thread:
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
class CloseThreadInput(TypedDict):
    thread: Thread
    is_closed: bool
```