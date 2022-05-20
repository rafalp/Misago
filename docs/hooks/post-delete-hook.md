# `post_delete_hook`

```python
from misago.graphql.post.hooks.postdelete import post_delete_hook

post_delete_hook.call_action(
    action: PostDeleteAction,
    context: Context,
    cleaned_data: PostDeleteInput,
)
```

A filter for the function used by `postDelete` GraphQL mutation to delete the reply from the database.

Returns `Thread` with updated thread data.


## Required arguments

### `action`

```python
async def delete_thread_post(
    context: Context, cleaned_data: PostDeleteInput
) -> Thread:
    ...
```

Next filter or built-in function used to delete the thread reply from the database.


### `context`

```python
Context
```

A dict with GraphQL query context.


### `cleaned_data`

```python
Dict[str, Any]
```

A dict with already validated and cleaned input data. Will contain `thread` and `post` keys:

```python
class PostDeleteInput(TypedDict):
    thread: Thread
    post: Post
```