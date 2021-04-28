from datetime import datetime
from typing import Any, Awaitable, Dict, Optional, Protocol

from ...graphql import GraphQLContext
from ...hooks import FilterHook
from ...richtext import RichText
from ...users.models import User
from ..models import Post, Thread


class CreatePostAction(Protocol):
    async def __call__(
        self,
        thread: Thread,
        markup: str,
        rich_text: RichText,
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
        *,
        poster: Optional[User] = None,
        poster_name: Optional[str] = None,
        edits: Optional[int] = 0,
        posted_at: Optional[datetime] = None,
        extra: Optional[Dict[str, Any]] = None,
        context: Optional[GraphQLContext] = None,
    ) -> Post:
        ...


class CreatePostHook(FilterHook[CreatePostAction, CreatePostFilter]):
    def call_action(
        self,
        action: CreatePostAction,
        thread: Thread,
        markup: str,
        rich_text: RichText,
        *,
        poster: Optional[User] = None,
        poster_name: Optional[str] = None,
        edits: Optional[int] = 0,
        posted_at: Optional[datetime] = None,
        extra: Optional[Dict[str, Any]] = None,
        context: Optional[GraphQLContext] = None,
    ) -> Awaitable[Post]:
        return self.filter(
            action,
            thread,
            markup,
            rich_text,
            poster=poster,
            poster_name=poster_name,
            edits=edits,
            posted_at=posted_at,
            extra=extra,
            context=context,
        )


create_post_hook = CreatePostHook()
