# `post_update_hook`

```python
from misago.graphql.public.mutations.hooks.postupdate import post_update_hook

post_update_hook.call_action(
    action: PostUpdateAction,
    context: GraphQLContext,
    cleaned_data: PostUpdateInput,
)
```

A filter for the function used by `postUpdate` GraphQL mutation to update the post in the database.

Returns tuple with `Post` dataclass with updated post data and `ParsedMarkupMetadata` being Python `dict` with metadata for parsed message.


## Required arguments

### `action`

```python
async def post_update(
    context: GraphQLContext, cleaned_data: PostUpdateInput
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
class PostUpdateInput(TypedDict):
    post: Post
    markup: str
```