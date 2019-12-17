from dataclasses import replace
from datetime import datetime
from typing import Any, Dict, Optional

from ..database.queries import update
from ..tables import posts, threads
from ..types import Category, Post, Thread, User
from ..utils.strings import slugify
from .ordering import get_ordering


async def update_post(
    post: Post,
    *,
    category: Optional[Category] = None,
    thread: Optional[Thread] = None,
    body: Optional[dict] = None,
    poster: Optional[User] = None,
    poster_name: Optional[str] = None,
    edits: Optional[int] = None,
    increment_edits: Optional[bool] = False,
    posted_at: Optional[datetime] = None,
    extra: Optional[dict] = None,
) -> Post:
    changes: Dict[str, Any] = {}

    if category and thread:
        raise ValueError("'category' and 'thread' options are mutually exclusive")
    if category and category.id != post.category_id:
        changes["category_id"] = category.id
    if thread and thread.id != post.thread_id:
        changes["thread_id"] = thread.id
    if thread and thread.category_id != post.category_id:
        changes["category_id"] = thread.category_id

    if body is not None and body != post.body:
        changes["body"] = body

    if poster:
        if poster_name:
            raise ValueError(
                "'poster' and 'poster_name' options are mutually exclusive"
            )
        if poster.id != post.poster_id:
            changes["poster_id"] = poster.id
        if poster.name != post.poster_name:
            changes["poster_name"] = poster.name
    elif poster_name:
        if post.poster_id:
            changes["poster_id"] = None
        if poster_name != post.poster_name:
            changes["poster_name"] = poster_name

    if edits is not None and increment_edits:
        raise ValueError("'edits' and 'increment_edits' options are mutually exclusive")
    if edits is not None and edits != post.edits:
        changes["edits"] = edits
    if increment_edits:
        changes["edits"] = posts.c.edits + 1

    if posted_at and posted_at != post.posted_at:
        changes["posted_at"] = posted_at

    if extra is not None and extra != post.extra:
        changes["extra"] = extra

    if not changes:
        return post

    await update(posts, post.id, **changes)

    if increment_edits:
        # replace SQL expression with actual int for use in new dataclass
        changes["edits"] = post.edits + 1

    updated_post = replace(post, **changes)
    return updated_post


async def update_thread(
    thread: Thread,
    *,
    category: Optional[Category] = None,
    first_post: Optional[Post] = None,
    starter: Optional[User] = None,
    starter_name: Optional[str] = None,
    last_post: Optional[Post] = None,
    last_poster: Optional[User] = None,
    last_poster_name: Optional[str] = None,
    title: Optional[str] = None,
    started_at: Optional[datetime] = None,
    last_posted_at: Optional[datetime] = None,
    replies: Optional[int] = None,
    increment_replies: Optional[bool] = False,
    is_closed: Optional[bool] = None,
    extra: Optional[dict] = None,
) -> Thread:
    changes: Dict[str, Any] = {}

    if category and category.id != thread.category_id:
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
        if first_post.id != thread.first_post_id:
            changes["first_post_id"] = first_post.id
        if first_post.poster_id != thread.starter_id:
            changes["starter_id"] = first_post.poster_id
        if first_post.poster_name != thread.starter_name:
            changes["starter_name"] = first_post.poster_name
        if first_post.posted_at != thread.started_at:
            changes["started_at"] = first_post.posted_at

    if starter:
        if starter_name:
            raise ValueError(
                "'starter' and 'starter_name' options are mutually exclusive"
            )
        if starter.id != thread.starter_id:
            changes["starter_id"] = starter.id
        if starter.name != thread.starter_name:
            changes["starter_name"] = starter.name
    elif starter_name:
        if thread.starter_id:
            changes["starter_id"] = None
        if starter_name != thread.starter_name:
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
        if last_post.id != thread.last_post_id:
            changes["last_post_id"] = last_post.id
        if last_post.poster_id != thread.last_poster_id:
            changes["last_poster_id"] = last_post.poster_id
        if last_post.poster_name != thread.last_poster_name:
            changes["last_poster_name"] = last_post.poster_name
        if last_post.posted_at != thread.last_posted_at:
            changes["last_posted_at"] = last_post.posted_at
            changes["ordering"] = get_ordering(last_post.posted_at)

    if last_poster:
        if last_poster_name:
            raise ValueError(
                "'last_poster' and 'last_poster_name' options are mutually exclusive"
            )
        if last_poster.id != thread.last_poster_id:
            changes["last_poster_id"] = last_poster.id
        if last_poster.name != thread.last_poster_name:
            changes["last_poster_name"] = last_poster.name
    elif last_poster_name:
        if thread.last_poster_id:
            changes["last_poster_id"] = None
        if last_poster_name != thread.last_poster_name:
            changes["last_poster_name"] = last_poster_name

    if title and title != thread.title:
        changes["title"] = title
        changes["slug"] = slugify(title)

    if started_at and started_at != thread.started_at:
        changes["started_at"] = started_at
    if last_posted_at and last_posted_at != thread.last_posted_at:
        changes["last_posted_at"] = last_posted_at
        changes["ordering"] = get_ordering(last_posted_at)

    if replies is not None and increment_replies:
        raise ValueError(
            "'replies' and 'increment_replies' options are mutually exclusive"
        )
    if replies is not None and replies != thread.replies:
        changes["replies"] = replies
    if increment_replies:
        changes["replies"] = threads.c.replies + 1

    if is_closed is not None and is_closed != thread.is_closed:
        changes["is_closed"] = is_closed

    if extra is not None and extra != thread.extra:
        changes["extra"] = extra

    if not changes:
        return thread

    await update(threads, thread.id, **changes)

    if increment_replies:
        # replace SQL expression with actual int for use in new dataclass
        changes["replies"] = thread.replies + 1

    updated_thread = replace(thread, **changes)
    return updated_thread
