# `post_reply_hook`

```python
post_reply_hook.call_action(
    action: PostReplyAction,
    context: GraphQLContext,
    cleaned_data: PostReplyInput,
)
```

A filter for the function used by GraphQL mutation creating new reply to create new reply in the database.

Returns tuple of `Thread` and `Post` dataclasses with newly created reply data.


## Required arguments

### `action`

```python
async def post_reply(
    context: GraphQLContext,
    cleaned_data: PostReplyInput,
) -> Tuple[Thread, Post]:
    ...
```

Next filter or built-in function used to create new reply in the database.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


### `cleaned_data`

```python
Dict[str, Any]
```

A dict with already validated and cleaned input data. Will contain at least `thread` and `body` keys:

```python
class PostReplyInput(TypedDict):
    thread: Thread
    body: str
```