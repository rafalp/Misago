from datetime import datetime
from typing import Optional, Protocol

from .category import Category
from .graphqlcontext import GraphQLContext
from .post import Post
from .richtext import RichText
from .thread import Thread
from .user import User


class UpdatePostAction(Protocol):
    async def __call__(
        self,
        post: Post,
        *,
        category: Optional[Category] = None,
        thread: Optional[Thread] = None,
        markup: Optional[str] = None,
        rich_text: Optional[RichText] = None,
        poster: Optional[User] = None,
        poster_name: Optional[str] = None,
        edits: Optional[int] = None,
        increment_edits: Optional[bool] = False,
        posted_at: Optional[datetime] = None,
        extra: Optional[dict] = None,
        context: Optional[GraphQLContext] = None,
    ) -> Post:
        ...


class UpdatePostFilter(Protocol):
    async def __call__(
        self,
        action: UpdatePostAction,
        post: Post,
        *,
        category: Optional[Category] = None,
        thread: Optional[Thread] = None,
        markup: Optional[str] = None,
        rich_text: Optional[RichText] = None,
        poster: Optional[User] = None,
        poster_name: Optional[str] = None,
        edits: Optional[int] = None,
        increment_edits: Optional[bool] = False,
        posted_at: Optional[datetime] = None,
        extra: Optional[dict] = None,
        context: Optional[GraphQLContext] = None,
    ) -> Post:
        ...
