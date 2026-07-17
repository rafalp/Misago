import html

import pytest
from django.utils.crypto import get_random_string

from ..core.utils import slugify
from ..threads.models import Post, Thread
from .utils import (
    FactoryTimestampArg,
    FactoryUserArg,
    factory_timestamp_arg,
    unpack_factory_user_arg,
)

__all__ = ["post_factory", "thread_reply_factory"]


@pytest.fixture
def post_factory():
    def _post_factory(
        thread: Thread,
        *,
        poster: FactoryUserArg = "Poster",
        original: str | None = None,
        parsed: str | None = None,
        metadata: dict | None = None,
        posted_at: FactoryTimestampArg = True,
        updated_at: FactoryTimestampArg = None,
        edits: int = 0,
        last_editor: FactoryUserArg = None,
        is_locked: bool = False,
        locked_at: FactoryTimestampArg = None,
        locked_by: FactoryUserArg = None,
        lock_reason: str | None = None,
        is_hidden: bool = False,
        hidden_at: FactoryTimestampArg = None,
        hidden_by: FactoryUserArg = None,
        hide_reason: str | None = None,
        has_reports: bool = False,
        has_open_reports: bool = False,
        is_unapproved: bool = False,
        search_document: str | None = None,
    ):
        poster_obj, poster_name, _ = unpack_factory_user_arg(poster)
        last_editor_obj, last_editor_name, last_editor_slug = unpack_factory_user_arg(
            last_editor
        )
        locked_by_obj, locked_by_name, locked_by_slug = unpack_factory_user_arg(
            locked_by
        )
        hidden_by_obj, hidden_by_name, hidden_by_slug = unpack_factory_user_arg(
            hidden_by
        )

        if not original:
            original = f"{get_random_string(4)} {get_random_string(4)}"
        if not parsed:
            parsed = f"<p>{original}</p>"
        if not search_document:
            search_document = original

        return Post.objects.create(
            category=thread.category,
            thread=thread,
            poster=poster_obj,
            poster_name=poster_name,
            original=original,
            parsed=parsed,
            metadata=metadata or {},
            posted_at=factory_timestamp_arg(posted_at),
            updated_at=factory_timestamp_arg(updated_at),
            edits=edits,
            last_editor=last_editor_obj,
            last_editor_name=last_editor_name,
            last_editor_slug=last_editor_slug,
            is_locked=is_locked,
            locked_at=factory_timestamp_arg(locked_at),
            locked_by=locked_by_obj,
            locked_by_name=locked_by_name,
            locked_by_slug=locked_by_slug,
            lock_reason=lock_reason,
            is_hidden=is_hidden,
            hidden_at=factory_timestamp_arg(hidden_at),
            hidden_by=hidden_by_obj,
            hidden_by_name=hidden_by_name,
            hidden_by_slug=hidden_by_slug,
            hide_reason=hide_reason,
            has_reports=has_reports,
            has_open_reports=has_open_reports,
            is_unapproved=is_unapproved,
            search_document=search_document,
        )

    return _post_factory


@pytest.fixture
def thread_reply_factory(post_factory):
    def _thread_reply_factory(
        thread: Thread,
        *,
        poster: FactoryUserArg = "Poster",
        original: str = "Hello world!",
        parsed: str | None = None,
        metadata: dict | None = None,
        posted_at: FactoryTimestampArg = True,
        updated_at: FactoryTimestampArg = None,
        edits: int = 0,
        last_editor: FactoryUserArg = None,
        is_locked: bool = False,
        locked_at: FactoryTimestampArg = None,
        locked_by: FactoryUserArg = None,
        lock_reason: str | None = None,
        is_hidden: bool = False,
        hidden_at: FactoryTimestampArg = None,
        hidden_by: FactoryUserArg = None,
        hide_reason: str | None = None,
        has_reports: bool = False,
        has_open_reports: bool = False,
        is_unapproved: bool = False,
        search_document: str | None = None,
        commit: bool = True,
    ):
        if not parsed:
            parsed = f"<p>{html.escape(original)}</p>"

        post = post_factory(
            thread,
            poster=poster,
            original=original,
            parsed=parsed,
            metadata=metadata,
            posted_at=posted_at,
            updated_at=updated_at,
            edits=edits,
            last_editor=last_editor,
            has_reports=has_reports,
            has_open_reports=has_open_reports,
            is_locked=is_locked,
            locked_at=locked_at,
            locked_by=locked_by,
            lock_reason=lock_reason,
            is_hidden=is_hidden,
            hidden_at=hidden_at,
            hidden_by=hidden_by,
            hide_reason=hide_reason,
            is_unapproved=is_unapproved,
            search_document=search_document,
        )

        if post.poster:
            poster_slug = post.poster.slug
        else:
            poster_slug = slugify(post.poster_name)

        thread.replies += 1
        thread.last_post = post
        thread.last_posted_at = post.posted_at
        thread.last_poster = post.poster
        thread.last_poster_name = post.poster_name
        thread.last_poster_slug = poster_slug

        if is_unapproved:
            thread.has_unapproved_posts = True
        if is_hidden:
            thread.has_hidden_posts = True

        if commit:
            thread.save()

        return post

    return _thread_reply_factory
