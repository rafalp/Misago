# `delete_thread_posts_hook`

```python
from misago.graphql.public.mutations.hooks.deletethreadposts import delete_thread_posts_hook

delete_thread_posts_hook.call_action(
    action: DeleteThreadPostsAction,
    context: GraphQLContext,
    cleaned_data: DeleteThreadPostsInput,
)
```

A filter for the function used by GraphQL mutation deleting thread posts to delete posts from the database.

Returns `Thread` with updated thread data.


## Required arguments

### `action`

```python
async def delete_thread_posts(
    context: GraphQLContext, cleaned_data: DeleteThreadPostsInput
) -> Thread:
    ...
```

Next filter or built-in function used to delete thread posts from the database.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


### `cleaned_data`

```python
Dict[str, Any]
```

A dict with already validated and cleaned input data. Will contain `thread` and `posts` keys:

```python
class DeleteThreadPostsInput(TypedDict):
    thread: Thread
    posts: List[Post]
```