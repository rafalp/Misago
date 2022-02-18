# `authenticate_user_hook`

```python
from misago.auth.hooks import authenticate_user_hook

authenticate_user_hook.call_action(
    action: AuthenticateUserAction,
    context: Context,
    username: str,
    password: str,
    in_admin: bool,
)
```

A filter for the function used to authenticate user for given user name/email and password.

Returns `User` dataclass with authenticated user data or `None` if user should not be able to authenticate (eg. inactive or invalid credentials).


## Required arguments

### `action`

```python
async def authenticate_user(
    context: Context,
    username: str,
    password: str,
    in_admin: str,
) -> Optional[User:]
    ...
```

Next filter or built-in function used to authenticate user for given credentials.


### `username`

```python
str
```

User name or e-mail address.


### `password`

```python
str
```

User password.


### `in_admin`

```python
bool
```

`True` if authentication is happening in the admin panel, `False` otherwise.