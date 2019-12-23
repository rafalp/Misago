from datetime import datetime
from typing import Any, Dict, Optional

from ..types import CreateUserAction, CreateUserFilter, GraphQLContext, User
from .filter import FilterHook


class CreateUserHook(FilterHook[CreateUserAction, CreateUserFilter]):
    async def call_action(
        self,
        action: CreateUserAction,
        name: str,
        email: str,
        *,
        password: Optional[str] = None,
        is_deactivated: bool = False,
        is_moderator: bool = False,
        is_admin: bool = False,
        joined_at: Optional[datetime] = None,
        extra: Optional[Dict[str, Any]] = None,
        context: Optional[GraphQLContext] = None,
    ) -> User:
        return await self.filter(
            action,
            name,
            email,
            password=password,
            is_deactivated=is_deactivated,
            is_moderator=is_moderator,
            is_admin=is_admin,
            joined_at=joined_at,
            extra=extra,
            context=context,
        )
