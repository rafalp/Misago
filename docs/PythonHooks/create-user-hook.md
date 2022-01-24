# `create_user_hook`

```python
from misago.users.hooks import create_user_hook

create_user_hook.call_action(
    action: CreateUserAction,
    name: str,
    email: str,
    *,
    full_name: Optional[str] = None,
    password: Optional[str] = None,
    is_active: bool = True,
    is_moderator: bool = False,
    is_admin: bool = False,
    joined_at: Optional[datetime] = None,
    extra: Optional[Dict[str, Any]] = None,
    context: Optional[GraphQLContext] = None,
)
```

A filter for the function used to create and setup new user account.

Returns `User` dataclass with newly created user data.


## Required arguments

### `action`

```python
async def create_user(
    name: str,
    email: str,
    *,
    full_name: Optional[str] = None,
    password: Optional[str] = None,
    is_active: bool = True,
    is_moderator: bool = False,
    is_admin: bool = False,
    joined_at: Optional[datetime] = None,
    extra: Optional[Dict[str, Any]] = None,
    context: Optional[GraphQLContext] = None,
) -> User:
    ...
```

Next filter or built-in function used to create new user account in the database.


### `name`

```python
str
```

User name.


### `email`

```python
str
```

User e-mail address.


## Optional arguments

### `full_name`

```python
Optional[str] = None
```

User's full name.


### `password`

```python
Optional[str] = None
```

User password. If not set, user will not be able to log-in to their account using default method.


### `is_active`

```python
bool = True
```

Controls if user's account is active.


### `is_moderator`

```python
bool = False
```

Controls if user can moderate site.


### `is_admin`

```python
bool = False
```

Controls if user user can administrate the site.


### `joined_at`

```python
Optional[datetime] = datetime.utcnow()
```

Joined at date for this user-account. Defaults to current date-time.


### `extra`

```python
Optional[Dict[str, Any]] = dict()
```

JSON-serializable dict with extra data for this user. This value is not used by Misago, but allows plugin authors to store additional information about user directly on their database row.


### `context`

```python
Optional[GraphQLContext]
```

A dict with GraphQL query context. Depending on where user is created may be unavailable and thus `None`.