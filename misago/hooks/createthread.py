from datetime import datetime
from typing import Any, Dict, Optional

from ..types import Category, CreateThreadAction, CreateThreadFilter, Post, Thread, User
from .filter import FilterHook


class CreateThreadHook(FilterHook[CreateThreadAction, CreateThreadFilter]):
    async def call_action(
        self,
        action: CreateThreadAction,
        category: Category,
        title: str,
        *,
        first_post: Optional[Post] = None,
        starter: Optional[User] = None,
        starter_name: Optional[str] = None,
        replies: int = 0,
        is_closed: bool = False,
        started_at: Optional[datetime] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> Thread:
        return await self.filter(
            action,
            category,
            title,
            first_post=first_post,
            starter=starter,
            starter_name=starter_name,
            replies=replies,
            is_closed=is_closed,
            started_at=started_at,
            extra=extra,
        )
