# `post_thread_hook`

```python
post_thread_hook.call_action(
    action: PostThreadAction,
    context: GraphQLContext,
    cleaned_data: PostThreadInput,
)
```

A filter for the function used by GraphQL mutation creating new thread to create new thread in the database.

Returns tuple of `Thread` and `Post` dataclasses with newly created thread data and `ParsedMarkupMetadata` being Python `dict` with metadata for parsed message.


## Required arguments

### `action`

```python
async def post_thread(
    context: GraphQLContext,
    cleaned_data: PostThreadInput,
) -> Tuple[Thread, Post, ParsedMarkupMetadata]:
    ...
```

Next filter or built-in function used to create new thread in the database.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


### `cleaned_data`

```python
Dict[str, Any]
```

A dict with already validated and cleaned input data. Will contain at least `category`, `title` and `markup` keys and optionally `is_closed` key:

```python
class PostThreadInput(TypedDict):
    category: Category
    title: str
    markup: str
    is_closed: Optional[bool]
```