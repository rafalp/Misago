from typing import Awaitable, Protocol

from ...hooks import FilterHook
from ..models import User


class DeleteUserContentAction(Protocol):
    async def __call__(
        self,
        user: User,
    ) -> User:
        ...


class DeleteUserContentFilter(Protocol):
    async def __call__(
        self,
        action: DeleteUserContentAction,
        user: User,
    ) -> User:
        ...


class DeleteUserContentHook(
    FilterHook[DeleteUserContentAction, DeleteUserContentFilter]
):
    def call_action(
        self,
        action: DeleteUserContentAction,
        user: User,
    ) -> Awaitable[User]:
        return self.filter(action, user)


delete_user_content_hook = DeleteUserContentHook()
