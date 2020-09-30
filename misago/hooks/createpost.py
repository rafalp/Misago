from datetime import datetime
from typing import Any, Dict, Optional

from ..types import (
    CreatePostAction,
    CreatePostFilter,
    GraphQLContext,
    Post,
    RichText,
    Thread,
    User,
)
from .filter import FilterHook


class CreatePostHook(FilterHook[CreatePostAction, CreatePostFilter]):
    async def call_action(
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
        return await self.filter(
            action,
            thread,
            markup,
            rich_text,
            html,
            poster=poster,
            poster_name=poster_name,
            edits=edits,
            posted_at=posted_at,
            extra=extra,
            context=context,
        )
