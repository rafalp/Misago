# `edit_thread_title_hook`

```python
edit_thread_title_hook.call_action(
    action: EditThreadTitleAction,
    context: GraphQLContext,
    cleaned_data: EditThreadTitleInput,
)
```

A filter for the function used by GraphQL mutation editing thread title to update the thread in the database.

Returns `Thread` dataclass with updated thread data.


## Required arguments

### `action`

```python
async def edit_thread_title(context: GraphQLContext, cleaned_data: EditThreadTitleInput) -> Thread:
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
class EditThreadTitleInput(TypedDict):
    thread: Thread
    title: str
```