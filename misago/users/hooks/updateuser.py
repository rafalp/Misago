from datetime import datetime
from typing import Any, Awaitable, Dict, Optional, Protocol

from ...graphql import GraphQLContext
from ...hooks import FilterHook
from ..models import User


class UpdateUserAction(Protocol):
    async def __call__(
        self,
        user: User,
        *,
        name: Optional[str] = None,
        email: Optional[str] = None,
        full_name: Optional[str] = None,
        password: Optional[str] = None,
        is_moderator: bool = False,
        is_admin: bool = False,
        joined_at: Optional[datetime] = None,
        extra: Optional[Dict[str, Any]] = None,
        context: Optional[GraphQLContext] = None,
    ) -> User:
        ...


class UpdateUserFilter(Protocol):
    async def __call__(
        self,
        action: UpdateUserAction,
        user: User,
        *,
        name: Optional[str] = None,
        email: Optional[str] = None,
        full_name: Optional[str] = None,
        password: Optional[str] = None,
        is_moderator: bool = False,
        is_admin: bool = False,
        joined_at: Optional[datetime] = None,
        extra: Optional[Dict[str, Any]] = None,
        context: Optional[GraphQLContext] = None,
    ) -> User:
        ...


class UpdateUserHook(FilterHook[UpdateUserAction, UpdateUserFilter]):
    def call_action(
        self,
        action: UpdateUserAction,
        user: User,
        *,
        name: Optional[str] = None,
        email: Optional[str] = None,
        full_name: Optional[str] = None,
        password: Optional[str] = None,
        is_active: bool = True,
        is_moderator: bool = False,
        is_admin: bool = False,
        joined_at: Optional[datetime] = None,
        extra: Optional[Dict[str, Any]] = None,
        context: Optional[GraphQLContext] = None,
    ) -> Awaitable[User]:
        return self.filter(
            action,
            user,
            name=name,
            email=email,
            full_name=full_name,
            password=password,
            is_active=is_active,
            is_moderator=is_moderator,
            is_admin=is_admin,
            joined_at=joined_at,
            extra=extra,
            context=context,
        )


update_user_hook = UpdateUserHook()
