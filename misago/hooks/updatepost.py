from datetime import datetime
from typing import Optional

from ..types import (
    UpdatePostAction,
    UpdatePostFilter,
    Category,
    GraphQLContext,
    Post,
    RichText,
    Thread,
    User,
)
from .filter import FilterHook


class UpdatePostHook(FilterHook[UpdatePostAction, UpdatePostFilter]):
    async def call_action(
        self,
        action: UpdatePostAction,
        post: Post,
        *,
        category: Optional[Category] = None,
        thread: Optional[Thread] = None,
        markup: Optional[str] = None,
        rich_text: Optional[RichText] = None,
        html: Optional[str] = None,
        poster: Optional[User] = None,
        poster_name: Optional[str] = None,
        edits: Optional[int] = None,
        increment_edits: Optional[bool] = False,
        posted_at: Optional[datetime] = None,
        extra: Optional[dict] = None,
        context: Optional[GraphQLContext] = None,
    ) -> Post:
        return await self.filter(
            action,
            post,
            category=category,
            thread=thread,
            markup=markup,
            rich_text=rich_text,
            html=html,
            poster=poster,
            poster_name=poster_name,
            edits=edits,
            increment_edits=increment_edits,
            posted_at=posted_at,
            extra=extra,
            context=context,
        )
