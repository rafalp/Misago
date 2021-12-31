# `update_post_hook`

```python
from misago.threads.hooks import update_post_hook

update_post_hook.call_action(
    action: UpdatePostAction,
    post: Post,
    *,
    category: Optional[Category] = None,
    thread: Optional[Thread] = None,
    markup: Optional[str] = None,
    rich_text: Optional[RichText] = None,
    poster: Optional[User] = None,
    poster_name: Optional[str] = None,
    edits: Optional[int] = None,
    increment_edits: Optional[bool] = False,
    posted_at: Optional[datetime] = None,
    extra: Optional[dict] = None,
    context: Optional[GraphQLContext] = None,
)
```

A filter for the function used to update existing post in the database.

Returns `Post` dataclass with updated post data.


## Required arguments

### `action`

```python
async def update_post(
    post: Post,
    *,
    category: Optional[Category] = None,
    thread: Optional[Thread] = None,
    markup: Optional[str] = None,
    rich_text: Optional[RichText] = None,
    poster: Optional[User] = None,
    poster_name: Optional[str] = None,
    edits: Optional[int] = None,
    increment_edits: Optional[bool] = False,
    posted_at: Optional[datetime] = None,
    extra: Optional[dict] = None,
    context: Optional[GraphQLContext] = None,
) -> Post:
    ...
```

Next filter or built-in function used to create new post in the database.


### `post`

```python
Post
```

`Post` dataclass representing post to update.


## Optional arguments


### `category`

```python
Category
```

`Category` dataclass with post's new category.


### `thread`

```python
Thread
```

`Thread` dataclass with post's new thread.


### `markup`

```python
Optional[str]
```

Python string with new raw unprocessed markup.


### `rich_text`

```python
Optional[RichText]
```

List of `dict` containing new JSON with rich text document representing parsed post body.


### `poster`

```python
Optional[User] = None
```

`User` dataclass with new post creator.


### `poster_names`

```python
Optional[str] = None
```

`str` with post creator name. Is mutually exclusive with `poster` argument. If given instead of `poster`, this means post creator was guest user.


### `edits`

```python
int = None
```

Number of times that post has been edited.

Mutually exclusive with `increment_edits` argument.


### `increment_edits`

```python
Optional[bool]
```

If `True`, delegates edits count increment to the database, avoiding potential race conditions.

Mutually exclusive with `edits` argument.


### `posted_at`

```python
Optional[datetime] = datetime.utcnow()
```

Updated `datetime` of post creation.


### `extra`

```python
Optional[Dict[str, Any]] = dict()
```

JSON-serializable dict with extra data for this post. This value is not used by Misago, but allows plugin authors to store additional information about post directly on it's database row.


### `context`

```python
Optional[GraphQLContext]
```

A dict with GraphQL query context. Depending on where post is updated may be unavailable and thus `None`.