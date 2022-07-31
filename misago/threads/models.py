from dataclasses import dataclass
from datetime import datetime
from typing import Any, Awaitable, Dict, Optional

from ..categories.models import Category
from ..database.models import Model, Query, mapper_registry, register_model
from ..richtext import RichText
from ..tables import posts, threads
from ..users.models import User
from ..utils import timezone
from ..utils.strings import slugify


@register_model(threads)
@dataclass
class Thread(Model):
    id: int
    category_id: int
    starter_name: str
    last_poster_name: str
    title: str
    slug: str
    started_at: datetime
    last_posted_at: datetime
    replies: int
    is_closed: bool
    extra: dict

    first_post_id: Optional[int]
    starter_id: Optional[int]
    last_post_id: Optional[int]
    last_poster_id: Optional[int]

    @property
    def posts_query(self) -> Query:
        return mapper_registry.query_model("Post").filter(thread_id=self.id)

    async def fetch_first_post(self) -> Optional["Post"]:
        if self.first_post_id:
            return await mapper_registry.query_model("Post").one(id=self.first_post_id)
        return None

    async def fetch_last_post(self) -> Optional["Post"]:
        if self.last_post_id:
            return await mapper_registry.query_model("Post").one(id=self.last_post_id)
        return None

    @classmethod
    def create(
        cls,
        category: Category,
        title: str,
        *,
        first_post: Optional["Post"] = None,
        starter: Optional[User] = None,
        starter_name: Optional[str] = None,
        replies: int = 0,
        is_closed: bool = False,
        started_at: Optional[datetime] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> Awaitable["Thread"]:
        if first_post:
            if starter:
                raise ValueError(
                    "'first_post' and 'starter' arguments are mutually exclusive"
                )
            if starter_name:
                raise ValueError(
                    "'first_post' and 'starter_name' arguments are mutually exclusive"
                )
            if started_at:
                raise ValueError(
                    "'first_post' and 'started_at' arguments are mutually exclusive"
                )

        if starter and starter_name:
            raise ValueError(
                "'starter' and 'starter_name' arguments are mutually exclusive"
            )

        if not (first_post or starter or starter_name):
            raise ValueError(
                "either 'first_post', 'starter' or 'starter_name' argument must be provided"
            )

        default_now = timezone.now()
        if first_post:
            started_at = first_post.posted_at
        else:
            started_at = started_at or default_now

        if first_post:
            starter_id = first_post.poster_id
            starter_name = first_post.poster_name
        elif starter:
            starter_id = starter.id
            starter_name = starter.name
        else:
            starter_id = None

        data: Dict[str, Any] = {
            "category_id": category.id,
            "first_post_id": first_post.id if first_post else None,
            "starter_id": starter_id,
            "starter_name": starter_name,
            "last_post_id": first_post.id if first_post else None,
            "last_poster_id": starter_id,
            "last_poster_name": starter_name,
            "title": title,
            "slug": slugify(title),
            "started_at": started_at,
            "last_posted_at": started_at,
            "replies": replies,
            "is_closed": is_closed,
            "extra": extra or {},
        }

        return cls.query.insert(**data)

    async def update(
        self,
        *,
        category: Optional[Category] = None,
        first_post: Optional["Post"] = None,
        starter: Optional[User] = None,
        starter_name: Optional[str] = None,
        last_post: Optional["Post"] = None,
        last_poster: Optional[User] = None,
        last_poster_name: Optional[str] = None,
        title: Optional[str] = None,
        started_at: Optional[datetime] = None,
        last_posted_at: Optional[datetime] = None,
        replies: Optional[int] = None,
        increment_replies: Optional[bool] = False,
        is_closed: Optional[bool] = None,
        extra: Optional[dict] = None,
    ) -> "Thread":
        changes: Dict[str, Any] = {}

        if category and category.id != self.category_id:
            changes["category_id"] = category.id

        if first_post:
            if starter:
                raise ValueError(
                    "'first_post' and 'starter' options are mutually exclusive"
                )
            if starter_name:
                raise ValueError(
                    "'first_post' and 'starter_name' options are mutually exclusive"
                )
            if started_at:
                raise ValueError(
                    "'first_post' and 'started_at' options are mutually exclusive"
                )
            if first_post.id != self.first_post_id:
                changes["first_post_id"] = first_post.id
            if first_post.poster_id != self.starter_id:
                changes["starter_id"] = first_post.poster_id
            if first_post.poster_name != self.starter_name:
                changes["starter_name"] = first_post.poster_name
            if first_post.posted_at != self.started_at:
                changes["started_at"] = first_post.posted_at

        if starter:
            if starter_name:
                raise ValueError(
                    "'starter' and 'starter_name' options are mutually exclusive"
                )
            if starter.id != self.starter_id:
                changes["starter_id"] = starter.id
            if starter.name != self.starter_name:
                changes["starter_name"] = starter.name
        elif starter_name:
            if self.starter_id:
                changes["starter_id"] = None
            if starter_name != self.starter_name:
                changes["starter_name"] = starter_name

        if last_post:
            if last_poster:
                raise ValueError(
                    "'last_post' and 'last_poster' options are mutually exclusive"
                )
            if last_poster_name:
                raise ValueError(
                    "'last_post' and 'last_poster_name' options are mutually exclusive"
                )
            if last_posted_at:
                raise ValueError(
                    "'last_post' and 'last_posted_at' options are mutually exclusive"
                )

            if last_post.id != self.last_post_id:
                changes["last_post_id"] = last_post.id
            if last_post.poster_id != self.last_poster_id:
                changes["last_poster_id"] = last_post.poster_id
            if last_post.poster_name != self.last_poster_name:
                changes["last_poster_name"] = last_post.poster_name
            if last_post.posted_at != self.last_posted_at:
                changes["last_posted_at"] = last_post.posted_at

        if last_poster:
            if last_poster_name:
                raise ValueError(
                    "'last_poster' and 'last_poster_name' options are mutually exclusive"
                )
            if last_poster.id != self.last_poster_id:
                changes["last_poster_id"] = last_poster.id
            if last_poster.name != self.last_poster_name:
                changes["last_poster_name"] = last_poster.name
        elif last_poster_name:
            if self.last_poster_id:
                changes["last_poster_id"] = None
            if last_poster_name != self.last_poster_name:
                changes["last_poster_name"] = last_poster_name

        if title and title != self.title:
            changes["title"] = title
            changes["slug"] = slugify(title)

        if started_at and started_at != self.started_at:
            changes["started_at"] = started_at
        if last_posted_at and last_posted_at != self.last_posted_at:
            changes["last_posted_at"] = last_posted_at

        if replies is not None and increment_replies:
            raise ValueError(
                "'replies' and 'increment_replies' options are mutually exclusive"
            )
        if replies is not None and replies != self.replies:
            changes["replies"] = replies
        if increment_replies:
            changes["replies"] = threads.c.replies + 1

        if is_closed is not None and is_closed != self.is_closed:
            changes["is_closed"] = is_closed

        if extra is not None and extra != self.extra:
            changes["extra"] = extra

        if not changes:
            return self

        await Thread.query.filter(id=self.id).update(**changes)

        if increment_replies:
            # replace SQL expression with actual int for use in new dataclass
            changes["replies"] = self.replies + 1

        return self.replace(**changes)

    def delete(self):
        return Thread.query.filter(id=self.id).delete()


@register_model(posts)
@dataclass
class Post(Model):
    id: int
    category_id: int
    thread_id: int
    poster_name: str
    markup: str
    rich_text: RichText
    edits: int
    posted_at: datetime
    extra: dict
    poster_id: Optional[int]

    @classmethod
    def create(
        cls,
        thread: Thread,
        markup: str = None,
        rich_text: RichText = None,
        *,
        poster: Optional[User] = None,
        poster_name: Optional[str] = None,
        edits: Optional[int] = 0,
        posted_at: Optional[datetime] = None,
        extra: Optional[dict] = None,
    ) -> Awaitable["Post"]:
        if poster and poster_name:
            raise ValueError(
                "'poster' and 'poster_name' arguments are mutually exclusive"
            )

        data: Dict[str, Any] = {
            "category_id": thread.category_id,
            "thread_id": thread.id,
            "poster_id": poster.id if poster else None,
            "poster_name": poster.name if poster else poster_name,
            "markup": markup or "",
            "rich_text": rich_text or [],
            "edits": edits,
            "posted_at": posted_at or timezone.now(),
            "extra": extra or {},
        }

        return cls.query.insert(**data)

    async def update(
        self,
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
    ) -> "Post":
        changes: Dict[str, Any] = {}

        if category and thread:
            raise ValueError("'category' and 'thread' options are mutually exclusive")
        if category and category.id != self.category_id:
            changes["category_id"] = category.id
        if thread and thread.id != self.thread_id:
            changes["thread_id"] = thread.id
        if thread and thread.category_id != self.category_id:
            changes["category_id"] = thread.category_id

        if markup is not None and markup != self.markup:
            changes["markup"] = markup
        if rich_text is not None and rich_text != self.rich_text:
            changes["rich_text"] = rich_text

        if poster:
            if poster_name:
                raise ValueError(
                    "'poster' and 'poster_name' options are mutually exclusive"
                )
            if poster.id != self.poster_id:
                changes["poster_id"] = poster.id
            if poster.name != self.poster_name:
                changes["poster_name"] = poster.name
        elif poster_name:
            if self.poster_id:
                changes["poster_id"] = None
            if poster_name != self.poster_name:
                changes["poster_name"] = poster_name

        if edits is not None and increment_edits:
            raise ValueError(
                "'edits' and 'increment_edits' options are mutually exclusive"
            )
        if edits is not None and edits != self.edits:
            changes["edits"] = edits
        if increment_edits:
            changes["edits"] = posts.c.edits + 1

        if posted_at and posted_at != self.posted_at:
            changes["posted_at"] = posted_at

        if extra is not None and extra != self.extra:
            changes["extra"] = extra

        if not changes:
            return self

        await Post.query.filter(id=self.id).update(**changes)

        if increment_edits:
            # replace SQL expression with actual int for use in new dataclass
            changes["edits"] = self.edits + 1

        return self.replace(**changes)

    def delete(self):
        return Post.query.filter(id=self.id).delete()
