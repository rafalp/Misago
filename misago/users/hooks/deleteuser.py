from typing import Awaitable, Optional, Protocol

from ...graphql import GraphQLContext
from ...hooks import FilterHook
from ..models import User


class DeleteUserAction(Protocol):
    async def __call__(
        self,
        user: User,
        *,
        context: Optional[GraphQLContext] = None,
    ) -> User:
        ...


class DeleteUserFilter(Protocol):
    async def __call__(
        self,
        action: DeleteUserAction,
        user: User,
        *,
        context: Optional[GraphQLContext] = None,
    ) -> User:
        ...


class DeleteUserHook(FilterHook[DeleteUserAction, DeleteUserFilter]):
    def call_action(
        self,
        action: DeleteUserAction,
        user: User,
        *,
        context: Optional[GraphQLContext] = None,
    ) -> Awaitable[User]:
        return self.filter(
            action,
            user,
            context=context,
        )


delete_user_hook = DeleteUserHook()
