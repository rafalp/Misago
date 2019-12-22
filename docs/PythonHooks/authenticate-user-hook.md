# `authenticate_user_hook`

```python
authenticate_user_hook.call_action(
    action: AuthenticateUserAction,
    context: GraphQLContext,
    username: str,
    password: str,
)
```

A filter for the function used to authenticate user for given user name/email and password.

Returns `User` dataclass with authenticated user data or `None` if user should not be able to authenticate (eg. deactivated or invalid credentials).


## Required arguments

### `action`

```python
async def authenticate_user(
    context: GraphQLContext,
    username: str,
    password: str,
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