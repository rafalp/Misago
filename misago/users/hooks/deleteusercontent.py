from datetime import datetime
from typing import Any, Awaitable, Dict, Optional, Protocol

from ...graphql import GraphQLContext
from ...hooks import FilterHook
from ..models import User


class DeleteUserContentAction(Protocol):
    async def __call__(
        self,
        user: User,
        *,
        context: Optional[GraphQLContext] = None,
    ) -> User:
        ...


class DeleteUserContentFilter(Protocol):
    async def __call__(
        self,
        action: DeleteUserContentAction,
        user: User,
        *,
        context: Optional[GraphQLContext] = None,
    ) -> User:
        ...


class DeleteUserContentHook(
    FilterHook[DeleteUserContentAction, DeleteUserContentFilter]
):
    def call_action(
        self,
        action: DeleteUserContentAction,
        user: User,
        *,
        context: Optional[GraphQLContext] = None,
    ) -> Awaitable[User]:
        return self.filter(
            action,
            user,
            context=context,
        )


delete_user_content_hook = DeleteUserContentHook()
