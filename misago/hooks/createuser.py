from datetime import datetime
from typing import Any, Awaitable, Dict, Optional, Protocol

from ..types import GraphQLContext, User
from .filter import FilterHook


class CreateUserAction(Protocol):
    async def __call__(
        self,
        name: str,
        email: str,
        *,
        password: Optional[str] = None,
        is_moderator: bool = False,
        is_administrator: bool = False,
        joined_at: Optional[datetime] = None,
        extra: Optional[Dict[str, Any]] = None,
        context: Optional[GraphQLContext] = None,
    ) -> User:
        ...


class CreateUserFilter(Protocol):
    async def __call__(
        self,
        action: CreateUserAction,
        name: str,
        email: str,
        *,
        password: Optional[str] = None,
        is_moderator: bool = False,
        is_administrator: bool = False,
        joined_at: Optional[datetime] = None,
        extra: Optional[Dict[str, Any]] = None,
        context: Optional[GraphQLContext] = None,
    ) -> User:
        ...


class CreateUserHook(FilterHook[CreateUserAction, CreateUserFilter]):
    def call_action(
        self,
        action: CreateUserAction,
        name: str,
        email: str,
        *,
        password: Optional[str] = None,
        is_active: bool = True,
        is_moderator: bool = False,
        is_administrator: bool = False,
        joined_at: Optional[datetime] = None,
        extra: Optional[Dict[str, Any]] = None,
        context: Optional[GraphQLContext] = None,
    ) -> Awaitable[User]:
        return self.filter(
            action,
            name,
            email,
            password=password,
            is_active=is_active,
            is_moderator=is_moderator,
            is_administrator=is_administrator,
            joined_at=joined_at,
            extra=extra,
            context=context,
        )


create_user_hook = CreateUserHook()
