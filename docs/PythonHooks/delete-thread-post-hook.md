# `delete_thread_post_hook`

```python
delete_thread_post_hook.call_action(
    action: DeleteThreadPostAction,
    context: GraphQLContext,
    cleaned_data: DeleteThreadPostInput,
)
```

A filter for the function used by GraphQL mutation deleting thread reply to delete the reply from the database.

Returns `Thread` with updated thread data.


## Required arguments

### `action`

```python
async def delete_thread_post(
    context: GraphQLContext, cleaned_data: DeleteThreadPostInput
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

A dict with already validated and cleaned input data. Will contain `thread` and `post` keys:

```python
class DeleteThreadPostInput(TypedDict):
    thread: Thread
    post: Post
```