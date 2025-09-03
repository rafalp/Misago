import pytest

from django.utils.crypto import get_random_string

from ..categories.models import Category
from ..threads.models import Thread
from ..core.utils import slugify
from .utils import (
    FactoryTimestampArg,
    FactoryUserArg,
    factory_timestamp_arg,
    unpack_factory_user_arg,
)

__all__ = ["thread_factory"]


@pytest.fixture
def thread_factory(post_factory):
    def _thread_factory(
        category: Category,
        *,
        title: str | None = None,
        replies: int = 0,
        has_events: bool = False,
        has_poll: bool = False,
        has_reported_posts: bool = False,
        has_open_reports: bool = False,
        has_unapproved_posts: bool = False,
        has_hidden_posts: bool = False,
        started_on: FactoryTimestampArg = True,
        last_post_on: FactoryTimestampArg = None,
        starter: FactoryUserArg = "Starter",
        last_poster: FactoryUserArg = None,
        weight: int = 0,
        is_unapproved: bool = False,
        is_hidden: bool = False,
        is_closed: bool = False,
    ):
        started_on = factory_timestamp_arg(started_on)
        if last_post_on is None:
            last_post_on = started_on
        else:
            last_post_on = factory_timestamp_arg(last_post_on)

        if not title:
            title = f"Thread {get_random_string(8)}"

        thread = Thread.objects.create(
            category=category,
            title=title,
            slug=slugify(title),
            replies=replies,
            has_events=has_events,
            has_poll=has_poll,
            has_reported_posts=has_reported_posts,
            has_open_reports=has_open_reports,
            has_unapproved_posts=has_unapproved_posts,
            has_hidden_posts=has_hidden_posts,
            started_on=started_on,
            last_post_on=last_post_on,
            weight=weight,
            is_unapproved=is_unapproved,
            is_hidden=is_hidden,
            is_closed=is_closed,
        )

        post = post_factory(
            thread,
            poster=starter,
            posted_at=started_on,
        )

        thread.first_post = post
        thread.last_post = post

        starter_obj, starter_name, starter_slug = unpack_factory_user_arg(starter)
        last_poster_obj, last_poster_name, last_poster_slug = unpack_factory_user_arg(
            last_poster or starter
        )

        thread.starter = starter_obj
        thread.starter_name = starter_name
        thread.starter_slug = starter_slug
        thread.last_poster = last_poster_obj
        thread.last_poster_name = last_poster_name
        thread.last_poster_slug = last_poster_slug

        thread.save()

        return thread

    return _thread_factory
