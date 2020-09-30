from datetime import datetime
from typing import Any, Dict, Optional, Protocol

from .graphqlcontext import GraphQLContext
from .post import Post
from .richtext import RichText
from .thread import Thread
from .user import User


class CreatePostAction(Protocol):
    async def __call__(
        self,
        thread: Thread,
        markup: str,
        rich_text: RichText,
        html: str,
        *,
        poster: Optional[User] = None,
        poster_name: Optional[str] = None,
        edits: Optional[int] = 0,
        posted_at: Optional[datetime] = None,
        extra: Optional[Dict[str, Any]] = None,
        context: Optional[GraphQLContext] = None,
    ) -> Post:
        ...


class CreatePostFilter(Protocol):
    async def __call__(
        self,
        action: CreatePostAction,
        thread: Thread,
        markup: str,
        rich_text: RichText,
        html: str,
        *,
        poster: Optional[User] = None,
        poster_name: Optional[str] = None,
        edits: Optional[int] = 0,
        posted_at: Optional[datetime] = None,
        extra: Optional[Dict[str, Any]] = None,
        context: Optional[GraphQLContext] = None,
    ) -> Post:
        ...
