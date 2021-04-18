from datetime import datetime
from typing import Any, Awaitable, Dict, Optional, Protocol

from ..types import (
    Category,
    GraphQLContext,
    Post,
    Thread,
    User,
)
from .filter import FilterHook


class CreateThreadAction(Protocol):
    async def __call__(
        self,
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
        context: Optional[GraphQLContext] = None,
    ) -> Thread:
        ...


class CreateThreadFilter(Protocol):
    async def __call__(
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
        context: Optional[GraphQLContext] = None,
    ) -> Thread:
        ...


class CreateThreadHook(FilterHook[CreateThreadAction, CreateThreadFilter]):
    def call_action(
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
        context: Optional[GraphQLContext] = None,
    ) -> Awaitable[Thread]:
        return self.filter(
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
            context=context,
        )


create_thread_hook = CreateThreadHook()
