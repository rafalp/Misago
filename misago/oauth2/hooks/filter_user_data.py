from typing import Optional, Protocol

from django.http import HttpRequest

from ...plugins.hooks import FilterHook
from ...users.models import User


class FilterUserDataHookAction(Protocol):
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
        *args,
        **kwargs,
    ) -> dict:
        return super().__call__(action, request, user, user_data, *args, **kwargs)


filter_user_data_hook = FilterUserDataHook()
