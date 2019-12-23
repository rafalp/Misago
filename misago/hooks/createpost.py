from datetime import datetime
from typing import Any, Dict, Optional

from ..types import (
    CreatePostAction,
    CreatePostFilter,
    GraphQLContext,
    Post,
    Thread,
    User,
)
from .filter import FilterHook


class CreatePostHook(FilterHook[CreatePostAction, CreatePostFilter]):
    async def call_action(
        self,
        action: CreatePostAction,
        thread: Thread,
        body: dict,
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
            body,
            poster=poster,
            poster_name=poster_name,
            edits=edits,
            posted_at=posted_at,
            extra=extra,
            context=context,
        )
