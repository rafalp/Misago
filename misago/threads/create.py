from datetime import datetime
from typing import Any, Dict, Optional

from ..database import queries
from ..tables import posts, threads
from ..types import Category, Post, Thread, User
from ..utils.strings import slugify


async def create_post(
    category: Category,
    thread: Thread,
    body: dict,
    *,
    poster: Optional[User] = None,
    poster_name: Optional[str] = None,
    edits: Optional[int] = 0,
    posted_at: Optional[datetime] = None,
    extra: Optional[dict] = None,
) -> Post:
    if poster and poster_name:
        raise ValueError("'poster' and 'poster_name' arguments are mutually exclusive")

    data: Dict[str, Any] = {
        "category_id": category.id,
        "thread_id": thread.id,
        "poster_id": poster.id if poster else None,
        "poster_name": poster.name if poster else poster_name,
        "body": body,
        "edits": edits,
        "posted_at": posted_at or datetime.utcnow(),
        "extra": extra or {},
    }

    data["id"] = await queries.insert(posts, **data)

    return Post(**data)


async def create_thread(
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

    default_now = datetime.utcnow()
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
        "ordering": int(started_at.timestamp()),
        "replies": replies,
        "is_closed": is_closed,
        "extra": extra or {},
    }

    data["id"] = await queries.insert(threads, **data)

    return Thread(**data)
