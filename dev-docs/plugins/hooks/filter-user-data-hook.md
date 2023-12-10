# `filter_user_data_hook`

This hook wraps the standard function used by Misago to filter a Python `dict` containing the user data retrieved from the OAuth 2 server.


## Location

This hook can be imported from `misago.oauth2.hooks`:

```python
from misago.oauth2.hooks import filter_user_data_hook
```


## Filter

Filter function implemented by a plugin must have the following signature:

```python
def custom_user_data_filter(
    action: FilterUserDataHookAction,
    request: HttpRequest,
    user: Optional[User],
    user_data: dict,
) -> dict:
    ...
```


## Action

Action callable passed as filter's `action` argument has the following signature:

```python
def filter_user_data_action(
    request: HttpRequest, user: Optional[User], user_data: dict
) -> dict:
    ...
```

### Arguments

#### `request: HttpRequest`

The request object.

#### `user: Optional[User]`

A `User` object associated with `user_data["id"]` or `user_data["email"]`. `None` if it's the user's first time signing in with OAuth and the user's account hasn't been created yet.

#### `user_data: dict`

A Python `dict` with user data extracted from the OAuth 2 server's response:

```python
class UserData(TypedDict):
    id: str
    name: str | None
    email: str | None
    avatar: str | None
```


## Example

This code extends standard filter logic with email normalization logic for Gmail domain:

```python
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

filter_user_data_hook.append(normalize_gmail_email)
```