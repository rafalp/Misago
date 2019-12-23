from datetime import datetime
from typing import Any, Dict, Optional, Protocol

from .category import Category
from .graphqlcontext import GraphQLContext
from .post import Post
from .thread import Thread
from .user import User


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
