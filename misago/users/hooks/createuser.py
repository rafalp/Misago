from datetime import datetime
from typing import Any, Awaitable, Dict, List, Optional, Protocol

from ...avatars.types import AvatarType
from ...context import Context
from ...hooks import FilterHook
from ..models import User


class CreateUserAction(Protocol):
    async def __call__(
        self,
        name: str,
        email: str,
        *,
        full_name: Optional[str] = None,
        password: Optional[str] = None,
        avatar_type: Optional[AvatarType] = None,
        avatars: Optional[List[dict]] = None,
        is_active: bool = True,
        is_moderator: bool = False,
        is_admin: bool = False,
        joined_at: Optional[datetime] = None,
        extra: Optional[Dict[str, Any]] = None,
        context: Optional[Context] = None,
    ) -> User:
        ...


class CreateUserFilter(Protocol):
    async def __call__(
        self,
        name: str,
        email: str,
        *,
        full_name: Optional[str] = None,
        password: Optional[str] = None,
        avatar_type: Optional[AvatarType] = None,
        avatars: Optional[List[dict]] = None,
        is_active: bool = True,
        is_moderator: bool = False,
        is_admin: bool = False,
        joined_at: Optional[datetime] = None,
        extra: Optional[Dict[str, Any]] = None,
        context: Optional[Context] = None,
    ) -> User:
        ...


class CreateUserHook(FilterHook[CreateUserAction, CreateUserFilter]):
    def call_action(
        self,
        action: CreateUserAction,
        name: str,
        email: str,
        *,
        full_name: Optional[str] = None,
        password: Optional[str] = None,
        avatar_type: Optional[AvatarType] = None,
        avatars: Optional[List[dict]] = None,
        is_active: bool = True,
        is_moderator: bool = False,
        is_admin: bool = False,
        joined_at: Optional[datetime] = None,
        extra: Optional[Dict[str, Any]] = None,
        context: Optional[Context] = None,
    ) -> Awaitable[User]:
        return self.filter(
            action,
            name,
            email,
            full_name=full_name,
            password=password,
            avatar_type=avatar_type,
            avatars=avatars,
            is_active=is_active,
            is_moderator=is_moderator,
            is_admin=is_admin,
            joined_at=joined_at,
            extra=extra,
            context=context,
        )


create_user_hook = CreateUserHook()
