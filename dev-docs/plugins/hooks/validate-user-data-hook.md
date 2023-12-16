# `validate_user_data_hook`

This hook wraps the standard function that Misago uses to validate a Python `dict` containing the user data extracted from the OAuth 2 server's response.

Raises Django's `ValidationError` if data is invalid.


## Location

This hook can be imported from `misago.oauth2.hooks`:

```python
from misago.oauth2.hooks import validate_user_data_hook
```


## Filter

```python
def custom_validate_user_data_filter(
    action: ValidateUserDataHookAction,
    request: HttpRequest,
    user: Optional[User],
    user_data: dict,
    response_json: dict,
) -> dict:
    ...
```

A function implemented by a plugin that can be registered in this hook.

Raises Django's `ValidationError` if data is invalid.


### Arguments

#### `action: ValidateUserDataHookAction`

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


#### `response_json: dict`

A Python `dict` with the unfiltered OAuth 2 server's user info JSON.


### Return value

A Python `dict` containing validated user data:

```python
class UserData(TypedDict):
    id: str
    name: str | None
    email: str | None
    avatar: str | None
```


## Action

```python
def validate_user_data_action(
    request: HttpRequest,
    user: Optional[User],
    user_data: dict,
    response_json: dict,
) -> dict:
    ...
```

A standard Misago function used for validating the user data, or the next filter function from another plugin.

Raises Django's `ValidationError` if data is invalid.


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


#### `response_json: dict`

A Python `dict` with the unfiltered OAuth 2 server's user info JSON.


### Return value

A Python `dict` containing validated user data:

```python
class UserData(TypedDict):
    id: str
    name: str | None
    email: str | None
    avatar: str | None
```


## Example

The code below implements a custom validation function that extends the standard logic with additional check for a permission to use the forum by the user:

```python
@validate_user_data_hook.append_filter
def normalize_gmail_email(
    action,
    request: HttpRequest,
    user: Optional[User],
    user_data: dict,
    response_json: dict,
) -> dict:
    if (
        not response_json.get("groups")
        or not isinstance(response_json["groups"], list)
        or not "forum" in response_json["groups"]
    ):
        raise ValidationError("You don't have a permission to use the forums.")

    # Call the next function in chain
    return action(user_data, request, user, user_data, response_json)
```