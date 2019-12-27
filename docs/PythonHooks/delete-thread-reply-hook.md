# `delete_thread_reply_hook`

```python
delete_thread_reply_hook.call_action(
    action: DeleteThreadReplyAction,
    context: GraphQLContext,
    cleaned_data: DeleteThreadReplyInput,
)
```

A filter for the function used by GraphQL mutation deleting thread reply to delete the reply from the database.

Returns `Thread` with updated thread data.


## Required arguments

### `action`

```python
async def delete_thread_reply(
    context: GraphQLContext, cleaned_data: DeleteThreadReplyInput
) -> Thread:
    ...
```

Next filter or built-in function used to delete the thread reply from the database.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


### `cleaned_data`

```python
Dict[str, Any]
```

A dict with already validated and cleaned input data. Will contain `thread` and `reply` keys:

```python
class DeleteThreadReplyInput(TypedDict):
    thread: Thread
    reply: Post
```