from typing import Optional, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...users.models import User


class ValidateUserDataHookAction(Protocol):
    def __call__(
        self,
        request: HttpRequest,
        user: Optional[User],
        user_data: dict,
        response_json: dict,
    ) -> dict:
        pass


class ValidateUserDataHookFilter(Protocol):
    def __call__(
        self,
        action: ValidateUserDataHookAction,
        request: HttpRequest,
        user: Optional[User],
        user_data: dict,
        response_json: dict,
    ) -> dict:
        pass


class ValidateUserDataHook(
    FilterHook[ValidateUserDataHookAction, ValidateUserDataHookFilter]
):
    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: ValidateUserDataHookAction,
        request: HttpRequest,
        user: Optional[User],
        user_data: dict,
        response_json: dict,
        *args,
        **kwargs,
    ) -> dict:
        return super().__call__(
            action, request, user, user_data, response_json, *args, **kwargs
        )


validate_user_data_hook = ValidateUserDataHook()
