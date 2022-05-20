# `post_create_hook`

```python
from misago.graphql.post.hooks.postcreate import post_create_hook

post_create_hook.call_action(
    action: PostCreateAction,
    context: Context,
    cleaned_data: PostCreateInput,
)
```

A filter for the function used by `postCreate` GraphQL mutation creating new thread reply.

Returns tuple of `Thread`, `Post` dataclasses with newly created reply data and `ParsedMarkupMetadata` being Python `dict` with metadata for parsed message.


## Required arguments

### `action`

```python
async def post_create(
    context: Context,
    cleaned_data: PostCreateInput,
) -> Tuple[Thread, Post, ParsedMarkupMetadata]:
    ...
```

Next filter or built-in function used to create new reply in the database.


### `context`

```python
Context
```

A dict with GraphQL query context.


### `cleaned_data`

```python
Dict[str, Any]
```

A dict with already validated and cleaned input data. Will contain at least `thread` and `markup` keys:

```python
class PostCreateInput(TypedDict):
    thread: Thread
    markup: str
```