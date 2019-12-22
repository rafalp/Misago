# `create_thread_hook`

```python
create_thread_hook.call_action(
    action: CreateThreadAction,
    category: Category,
    title: str,
    *,
    first_post: Optional[Post] = None,
    starter: Optional[User] = None,
    starter_name: Optional[str] = None,
    replies: int = 0,
    is_closed: bool = False,
    started_at: Optional[datetime] = None,
    extra: Optional[Dict[str, Any]] = None,
)
```

A filter for the function used to create new thread in the database.

Returns `Thread` dataclass with newly created thread data.

> **Note:** Misago requires for thread to exist in the database before thread first post can be created. Most of times this method will be called with `first_post` being empty and updated later.


## Required arguments

### `action`

```python
async def create_thread(
    category: Category,
    title: str,
    *,
    first_post: Optional[Post] = None,
    starter: Optional[User] = None,
    starter_name: Optional[str] = None,
    replies: int = 0,
    is_closed: bool = False,
    started_at: Optional[datetime] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> Thread:
    ...
```

Next filter or built-in function used to create new thread in the database.


### `category`

```python
Category
```

`Category` dataclass for category in which thread will be created.


### `title`

```python
str
```

String with thread title.


## Optional arguments

### `first_post`

```python
Optional[Post] = None
```

`Post` dataclass with thread first post.


### `starter`

```python
Optional[User] = None
```

`User` dataclass with thread starter.


### `starter_name`

```python
Optional[str] = None
```

`str` with thread starter name. Is mutually exclusive with `starter` argument. If given instead of `starter`, this means thread creator was guest user.


### `replies`

```python
int = False
```

Initial count of thread replies.


###  `is_closed`

```python
bool = False
```

Controls if thread should be created closed.


### `started_at`

```python
Optional[datetime]
```

`datetime` of thread creation. Mutually exclusive with `first_post`. If `first_post` is given, it's `posted_at` `datetime` will be used instead.


### `extra`

```python
Optional[Dict[str, Any]] = dict()
```

JSON-serializable dict with extra data for this thread. This value is not used by Misago, but allows plugin authors to store additional information about thread directly on it's database row.