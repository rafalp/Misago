from dataclasses import replace
from datetime import datetime
from typing import Any, Dict, Optional

from ..database.queries import update
from ..tables import threads
from ..types import Category, Post, Thread, User
from ..utils.strings import slugify


async def update_thread(
    thread: Thread,
    *,
    category: Optional[Category] = None,
    first_post: Optional[Post] = None,
    starter: Optional[User] = None,
    last_poster: Optional[User] = None,
    title: Optional[str] = None,
    started_at: Optional[datetime] = None,
    last_posted_at: Optional[datetime] = None,
    replies: Optional[int] = None,
    is_closed: Optional[bool] = None,
    extra: Optional[dict] = None,
) -> Thread:
    changes: Dict[str, Any] = {}

    if category and category.id != thread.category_id:
        changes["category_id"] = category.id

    if first_post and first_post.id != thread.first_post_id:
        changes["first_post_id"] = first_post.id

    if starter:
        if starter.id != thread.starter_id:
            changes["starter_id"] = starter.id
            changes["starter_name"] = starter.name
        elif starter.name != thread.starter_name:
            changes["starter_name"] = starter.name

    if last_poster:
        if last_poster.id != thread.last_poster_id:
            changes["last_poster_id"] = last_poster.id
            changes["last_poster_name"] = last_poster.name
        elif last_poster.name != thread.last_poster_name:
            changes["last_poster_name"] = last_poster.name

    if title and title != thread.title:
        changes["title"] = title
        changes["slug"] = slugify(title)

    if started_at and started_at != thread.started_at:
        changes["started_at"] = started_at
    if last_posted_at and last_posted_at != thread.last_posted_at:
        changes["last_posted_at"] = last_posted_at
        changes["ordering"] = int(last_posted_at.timestamp())

    if replies is not None and replies != thread.replies:
        changes["replies"] = replies

    if is_closed is not None and is_closed != thread.is_closed:
        changes["is_closed"] = is_closed

    if extra is not None and extra != thread.extra:
        changes["extra"] = extra

    if not changes:
        return thread

    await update(threads, thread.id, **changes)
    updated_thread = replace(thread, **changes)
    return updated_thread
