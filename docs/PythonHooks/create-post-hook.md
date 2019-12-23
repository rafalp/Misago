# `create_post_hook`

```python
create_post_hook.call_action(
    action: CreatePostAction,
    thread: Thread,
    body: dict,
    *,
    poster: Optional[User] = None,
    poster_name: Optional[str] = None,
    edits: Optional[int] = 0,
    posted_at: Optional[datetime] = None,
    extra: Optional[dict] = None,
    context: Optional[GraphQLContext] = None,
)
```

A filter for the function used to create new post in the database.

Returns `Post` dataclass with newly created post data.


## Required arguments

### `action`

```python
async def create_post(
    thread: Thread,
    body: dict,
    *,
    poster: Optional[User] = None,
    poster_name: Optional[str] = None,
    edits: Optional[int] = 0,
    posted_at: Optional[datetime] = None,
    extra: Optional[dict] = None,
    context: Optional[GraphQLContext] = None,
) -> Thread:
    ...
```

Next filter or built-in function used to create new post in the database.


### `thread`

```python
Thread
```

`Thread` dataclass for thread in which thread will be created.


### `body`

```python
dict
```

`dict` containing JSON with [ProseMirror](https://prosemirror.net) document representing post body.


## Optional arguments

### `poster`

```python
Optional[User] = None
```

`User` dataclass with post creator.


### `starter_name`

```python
Optional[str] = None
```

`str` with post creator name. Is mutually exclusive with `poster` argument. If given instead of `poster`, this means post creator was guest user.


### `edits`

```python
int = False
```

Initial count of number of times that post has been edited.


### `posted_at`

```python
Optional[datetime] = datetime.utcnow()
```

`datetime` of post creation.


### `extra`

```python
Optional[Dict[str, Any]] = dict()
```

JSON-serializable dict with extra data for this post. This value is not used by Misago, but allows plugin authors to store additional information about post directly on it's database row.


### `context`

```python
Optional[GraphQLContext]
```

A dict with GraphQL query context. Depending on where post is created may be unavailable and thus `None`.