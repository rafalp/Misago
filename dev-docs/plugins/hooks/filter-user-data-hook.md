# `filter_user_data_hook`

This hook wraps the standard function used by Misago to filter a Python `dict` containing the user data retrieved from the OAuth 2 server.

`filter_user_data_hook` is a **filter** hook.


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

Misago's standard function used to filter the user's data, or a next filter in line.


## Example

This code extends standard filter logic with email normalization logic for Gmail domain:

```python
def normalize_gmail_email(
    action, request: HttpRequest, user: Optional[User], user_data: dict
) -> dict:
    if (
        isinstance(user_data.get("email"), str)
        and user_data["email"].lower().endswith("@gmail.com")
    ):
        new_user_data = user_data.copy()
        # Dots in Gmail emails are ignored but frequently used by spammers
        new_user_email = user_data["email"][:-10].replace(".", "")
        new_user_data["email"] = new_user_email + "@gmail.com"
        return action(new_user_data, request, user, user_data)

    return action(user_data, request, user, user_data)

filter_user_data_hook.append(normalize_gmail_email)
```