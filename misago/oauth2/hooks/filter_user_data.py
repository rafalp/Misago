from typing import Optional, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...users.models import User


class FilterUserDataHookAction(Protocol):
    """
    # Arguments

    ## `request: HttpRequest`

    The request object.

    ## `user: Optional[User]`

    A `User` object associated with `user_data["id"]` or `user_data["email"]`.
    `None` if it's the user's first time signing in with OAuth and the user's
    account hasn't been created yet.

    ## `user_data: dict`

    A Python `dict` with user data extracted from the OAuth 2 server's response:

    ```python
    class UserData(TypedDict):
        id: str
        name: str | None
        email: str | None
        avatar: str | None
    ```
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
    """
    This hook wraps the standard function used by Misago to filter a Python `dict`
    containing the user data retrieved from the OAuth 2 server.

    # Example

    This code extends standard filter logic with email normalization logic for
    Gmail domain:

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
    """

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
