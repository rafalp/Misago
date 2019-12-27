# `delete_thread_replies_hook`

```python
delete_thread_replies_hook.call_action(
    action: DeleteThreadRepliesAction,
    context: GraphQLContext,
    cleaned_data: DeleteThreadRepliesInput,
)
```

A filter for the function used by GraphQL mutation deleting thread replies to delete replies from the database.

Returns `Thread` with updated thread data.


## Required arguments

### `action`

```python
async def delete_thread_replies(
    context: GraphQLContext, cleaned_data: DeleteThreadRepliesInput
) -> Thread:
    ...
```

Next filter or built-in function used to delete thread replies from the database.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


### `cleaned_data`

```python
Dict[str, Any]
```

A dict with already validated and cleaned input data. Will contain `thread` and `replies` keys:

```python
class DeleteThreadRepliesInput(TypedDict):
    thread: Thread
    replies: List[Post]
```