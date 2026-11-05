from typing import Protocol

from ...plugins.hooks import FilterHook
from ..models import User


class AnonymizeUserDataHookAction(Protocol):
    def __call__(
        self,
        user: User,
        anonymous_username: str,
    ) -> None: ...


class AnonymizeUserDataHookFilter(Protocol):
    def __call__(
        self,
        action: AnonymizeUserDataHookAction,
        user: User,
        anonymous_username: str,
    ) -> None: ...


class AnonymizeUserDataHook(
    FilterHook[
        AnonymizeUserDataHookAction,
        AnonymizeUserDataHookFilter,
    ]
):
    __slots__ = FilterHook.__slots__

    def __call__(
        self,
        action: AnonymizeUserDataHookAction,
        user: User,
        anonymous_username: str,
    ) -> None:
        return super().__call__(
            action,
            user,
            anonymous_username,
        )


anonymize_user_data_hook = AnonymizeUserDataHook()
