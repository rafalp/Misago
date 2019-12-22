# `close_thread_input_model_hook`

```python
close_thread_input_model_hook.call_action(action: CloseThreadInputModelAction, context: GraphQLContext)
```

A filter for the function used to create [input model](https://pydantic-docs.helpmanual.io/usage/models/) for `CloseThreadInputModel` GraphQL input type used by the "thread reply" GraphQL mutation.

Returns `CloseThreadInputModel` input model type.


## Required arguments

### `action`

```python
async def create_input_model(context: GraphQLContext) -> CloseThreadInputModel:
    ...
```

Next filter or built-in function used to create input model type.


### `context`

```python
GraphQLContext
```

A dict with GraphQL query context.


- - -


# `create_post_hook`:

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