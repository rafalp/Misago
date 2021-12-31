# `edit_post_hook`

```python
from misago.graphql.public.mutations.hooks.editpost import edit_post_hook

edit_post_hook.call_action(
    action: EditPostAction,
    context: GraphQLContext,
    cleaned_data: EditPostInput,
)
```

A filter for the function used by GraphQL mutation editing post to update the post in the database.

Returns tuple with `Post` dataclass with updated post data and `ParsedMarkupMetadata` being Python `dict` with metadata for parsed message.


## Required arguments

### `action`

```python
async def edit_post(
    context: GraphQLContext, cleaned_data: EditPostInput
) -> Tuple[Post, ParsedMarkupMetadata]:
    ...
```

Next filter or built-in function used to update the post in the database.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


### `cleaned_data`

```python
Dict[str, Any]
```

A dict with already validated and cleaned input data. Will contain at least `post` and `markup` keys:

```python
class EditPostInput(TypedDict):
    post: Post
    markup: str
```