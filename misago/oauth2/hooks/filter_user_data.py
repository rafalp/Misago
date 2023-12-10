"""
This hook wraps the standard function used by Misago to filter a Python `dict` containing the user data retrieved from the OAuth 2 server.

# Example

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
"""

from typing import Optional, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...users.models import User


class FilterUserDataHookAction(Protocol):
    """
    Misago's standard function used to filter the user's data, or a next filter in line.
    """

    def __call__(
        self,
        request: HttpRequest,
        user: Optional[User],
        user_data: dict,
    ) -> dict:
        pass


class FilterUserDataHookFilter(Protocol):
    def __call__(
        self,
        action: FilterUserDataHookAction,
        request: HttpRequest,
        user: Optional[User],
        user_data: dict,
    ) -> dict:
        pass


class FilterUserDataHook(
    FilterHook[FilterUserDataHookAction, FilterUserDataHookFilter]
):
    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: FilterUserDataHookAction,
        request: HttpRequest,
        user: Optional[User],
        user_data: dict,
    ) -> dict:
        return super().__call__(action, request, user, user_data)


filter_user_data_hook = FilterUserDataHook()
