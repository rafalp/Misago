# `filter_user_data_hook`

This hook wraps the standard function that Misago uses to filter a Python `dict` containing the user data extracted from the OAuth 2 server's response.


## Location

This hook can be imported from `misago.oauth2.hooks`:

```python
from misago.oauth2.hooks import filter_user_data_hook
```


## Filter

```python
def custom_user_data_filter(
    action: FilterUserDataHookAction,
    request: HttpRequest,
    user: Optional[User],
    user_data: dict,
) -> dict:
    ...
```

A function implemented by a plugin that can be registered in this hook.

### Arguments

#### `action: FilterUserDataHookAction`

Built in function used by Misago to filter user data, or next filter.

See the [action](#action) section for details.

#### `request: HttpRequest`

The request object.

#### `user: Optional[User]`

A `User` object associated with `user_data["id"]` or `user_data["email"]`.
`None` if it's the user's first time signing in with OAuth and the user's
account hasn't been created yet.

#### `user_data: dict`

A Python `dict` with user data extracted from the OAuth 2 server's response:

```python
class UserData(TypedDict):
    id: str
    name: str | None
    email: str | None
    avatar: str | None
```

### Return value

A Python `dict` containing user data:

```python
class UserData(TypedDict):
    id: str
    name: str | None
    email: str | None
    avatar: str | None
```


## Action

```python
def filter_user_data_action(
    request: HttpRequest, user: Optional[User], user_data: dict
) -> dict:
    ...
```

A standard Misago function is used for filtering the user data, or a partial filter function from another plugin.

### Arguments

#### `request: HttpRequest`

The request object.

#### `user: Optional[User]`

A `User` object associated with `user_data["id"]` or `user_data["email"]`.
`None` if it's the user's first time signing in with OAuth and the user's
account hasn't been created yet.

#### `user_data: dict`

A Python `dict` with user data extracted from the OAuth 2 server's response:

```python
class UserData(TypedDict):
    id: str
    name: str | None
    email: str | None
    avatar: str | None
```

### Return value

A Python `dict` containing user data:

```python
class UserData(TypedDict):
    id: str
    name: str | None
    email: str | None
    avatar: str | None
```


## Example

The code below implements a custom filter function that extends the standard logic with additional user e-mail normalization for Gmail e-mails:

```python
@filter_user_data_hook.append_filter
def normalize_gmail_email(
    action, request: HttpRequest, user: Optional[User], user_data: dict
) -> dict:
    if (
        user_data["email"]
        and user_data["email"].lower().endswith("@gmail.com")
    ):
        # Dots in Gmail emails are ignored but frequently used by spammers
        new_user_email = user_data["email"][:-10].replace(".", "")
        user_data["email"] = new_user_email + "@gmail.com"

    return action(user_data, request, user, user_data)
```