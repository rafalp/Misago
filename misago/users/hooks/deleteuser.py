from typing import Awaitable, Protocol

from ...hooks import FilterHook
from ..models import User


class DeleteUserAction(Protocol):
    async def __call__(
        self,
        user: User,
    ) -> User:
        ...


class DeleteUserFilter(Protocol):
    async def __call__(
        self,
        action: DeleteUserAction,
        user: User,
    ) -> User:
        ...


class DeleteUserHook(FilterHook[DeleteUserAction, DeleteUserFilter]):
    def call_action(
        self,
        action: DeleteUserAction,
        user: User,
    ) -> Awaitable[User]:
        return self.filter(action, user)


delete_user_hook = DeleteUserHook()
