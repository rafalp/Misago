# `authenticate_admin_hook`

```python
authenticate_admin_hook.call_action(
    action: AuthenticateUserAction,
    context: GraphQLContext,
    username: str,
    password: str,
)
```

A filter for the function used to authenticate admin for given user name/email and password.

Returns `User` dataclass with authenticated admin data or `None` if user should not be able to authenticate (eg. not admin or invalid credentials).


## Required arguments

### `action`

```python
async def authenticate_admin(
    context: GraphQLContext,
    username: str,
    password: str,
) -> Optional[User:]
    ...
```

Next filter or built-in function used to authenticate admin for given credentials.


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