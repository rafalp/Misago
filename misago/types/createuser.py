from datetime import datetime
from typing import Any, Dict, Optional, Protocol

from .user import User


class CreateUserAction(Protocol):
    async def __call__(
        self,
        name: str,
        email: str,
        *,
        password: Optional[str] = None,
        is_moderator: bool = False,
        is_admin: bool = False,
        joined_at: Optional[datetime] = None,
        extra: Optional[Dict[str, Any]] = None,
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
        is_admin: bool = False,
        joined_at: Optional[datetime] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> User:
        ...
