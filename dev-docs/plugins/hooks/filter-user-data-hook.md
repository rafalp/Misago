# `filter_user_data_hook`

This hook wraps the standard function that Misago uses to filter a Python `dict` containing the user data extracted from the OAuth 2 server's response.

User data filtering is part of the [user data validation by the OAuth 2 client](./validate-user-data-hook.md), which itself is part of a function that creates a new user account or updates an existing one if user data has changed.

Standard user data filtering doesn't validate the data but instead tries to improve it to increase its chances of passing the validation. It converts the `name` into a valid Misago username (e.g., `Łukasz Kowalski` becomes `Lukasz_Kowalski`). It also appends a random string at the end of the name if it's already taken by another user (e.g., `RickSanchez` becomes `RickSanchez_C137`). If the name is empty, a placeholder one is generated, e.g., `User_d6a9`. Lastly, it replaces an `email` with an empty string if it's `None`, to prevent a type error from being raised by e-mail validation that happens in the next step.

Plugin filters can still raise Django's `ValidationError` on an invalid value instead of attempting to fix it if this is a preferable resolution.


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

A standard Misago function used for filtering the user data, or the next filter function from another plugin.

See the [action](#action) section for details.


#### `request: HttpRequest`

The request object.


#### `user: Optional[User]`

A `User` object associated with `user_data["id"]` or `user_data["email"]`, or `None` if it's the user's first time signing in with OAuth and the user's account hasn't been created yet.


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

A standard Misago function used for filtering the user data, or the next filter function from another plugin.


### Arguments

#### `request: HttpRequest`

The request object.


#### `user: Optional[User]`

A `User` object associated with `user_data["id"]` or `user_data["email"]`, or `None` if it's the user's first time signing in with OAuth and the user's account hasn't been created yet.


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
from django.http import HttpRequest
from misago.oauth.hooks import filter_user_data_hook
from misago.users.models import User


@filter_user_data_hook.append_filter
def normalize_gmail_email(
    action, request: HttpRequest, user: User | None, user_data: dict
) -> dict:
    if (
        user_data["email"]
        and user_data["email"].lower().endswith("@gmail.com")
    ):
        # Dots in Gmail emails are ignored but frequently used by spammers
        new_user_email = user_data["email"][:-10].replace(".", "")
        user_data["email"] = new_user_email + "@gmail.com"

    # Call the next function in chain
    return action(user_data, request, user, user_data)
```