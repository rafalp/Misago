# `posts_bulk_delete_hook`

```python
from misago.graphql.public.mutations.hooks.postsbulkdelete import posts_bulk_delete_hook

posts_bulk_delete_hook.call_action(
    action: PostsBulkDeleteAction,
    context: GraphQLContext,
    cleaned_data: PostsBulkDeleteInput,
)
```

A filter for the function used by `postsBulkDelete` GraphQL mutation to delete posts from the database.

Returns `Thread` with updated thread data.


## Required arguments

### `action`

```python
async def delete_thread_posts(
    context: GraphQLContext, cleaned_data: PostsBulkDeleteInput
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
class PostsBulkDeleteInput(TypedDict):
    thread: Thread
    posts: List[Post]
```