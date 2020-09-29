# `edit_post_hook`

```python
edit_post_hook.call_action(
    action: EditPostAction,
    context: GraphQLContext,
    cleaned_data: EditPostInput,
)
```

A filter for the function used by GraphQL mutation editing post to update the post in the database.

Returns `Post` dataclass with updated post data.


## Required arguments

### `action`

```python
async def edit_post(context: GraphQLContext, cleaned_data: EditPostInput) -> Post:
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