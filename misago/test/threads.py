from dataclasses import dataclass

import pytest
from django.utils.crypto import get_random_string

from ..attachments.models import Attachment
from ..categories.models import Category
from ..notifications.models import Notification, WatchedThread
from ..polls.models import Poll, PollVote
from ..readtracker.models import ReadThread
from ..threads.models import Post, Thread
from ..threadupdates.create import create_test_thread_update
from ..threadupdates.models import ThreadUpdate
from ..core.utils import slugify
from .utils import (
    FactoryTimestampArg,
    FactoryUserArg,
    factory_timestamp_arg,
    unpack_factory_user_arg,
)

__all__ = ["ThreadRelations", "thread_factory", "thread_relations_factory"]


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
        started_at: FactoryTimestampArg = True,
        last_posted_at: FactoryTimestampArg = None,
        starter: FactoryUserArg = "Starter",
        last_poster: FactoryUserArg = None,
        weight: int = 0,
        is_unapproved: bool = False,
        is_hidden: bool = False,
        is_closed: bool = False,
    ):
        started_at = factory_timestamp_arg(started_at)
        if last_posted_at is None:
            last_posted_at = started_at
        else:
            last_posted_at = factory_timestamp_arg(last_posted_at)

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
            started_at=started_at,
            last_posted_at=last_posted_at,
            weight=weight,
            is_unapproved=is_unapproved,
            is_hidden=is_hidden,
            is_closed=is_closed,
        )

        post = post_factory(
            thread,
            poster=starter,
            posted_at=started_at,
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


@pytest.fixture
def thread_relations_factory(user, other_user):
    def _thread_relations_factory(thread: Thread) -> "ThreadRelations":
        post = thread.first_post

        attachment = Attachment.objects.create(
            category=thread.category,
            thread=thread,
            post=post,
            uploader_name="Anonymous",
            uploader_slug="anonymous",
            name="filename.txt",
            slug="filename-txt",
        )

        notification = Notification.objects.create(
            user=user,
            verb="TEST",
            actor=other_user,
            actor_name=other_user.username,
            category=thread.category,
            thread=thread,
            thread_title=thread.title,
            post=post,
        )

        poll = Poll.objects.create(
            category=thread.category,
            thread=thread,
            starter=user,
            starter_name=user.username,
            starter_slug=user.slug,
            question="...",
            choices=[],
        )

        poll_vote = PollVote.objects.create(
            category=thread.category,
            thread=thread,
            poll=poll,
            choice_id="aaaa",
            voter=user,
            voter_name=user.username,
            voter_slug=user.slug,
        )

        read_thread = ReadThread.objects.create(
            user=user,
            category=thread.category,
            thread=thread,
        )

        thread_update = create_test_thread_update(thread, other_user)

        watched_thread = WatchedThread.objects.create(
            user=user,
            category=thread.category,
            thread=thread,
        )

        return ThreadRelations(
            attachment=attachment,
            notification=notification,
            poll=poll,
            poll_vote=poll_vote,
            post=post,
            read_thread=read_thread,
            thread_update=thread_update,
            watched_thread=watched_thread,
        )

    return _thread_relations_factory


@dataclass(frozen=True)
class ThreadRelations:
    attachment: Attachment
    notification: Notification
    poll: Poll
    poll_vote: PollVote
    post: Post
    read_thread: ReadThread
    thread_update: ThreadUpdate
    watched_thread: WatchedThread

    def assert_category(self, category: Category):
        self.attachment.refresh_from_db()
        assert self.attachment.category_id == category.id

        self.notification.refresh_from_db()
        assert self.notification.category_id == category.id

        self.poll.refresh_from_db()
        assert self.poll.category_id == category.id

        self.poll_vote.refresh_from_db()
        assert self.poll_vote.category_id == category.id

        self.read_thread.refresh_from_db()
        assert self.read_thread.category_id == category.id

        self.post.refresh_from_db()
        assert self.post.category_id == category.id

        self.thread_update.refresh_from_db()
        assert self.thread_update.category_id == category.id

        self.watched_thread.refresh_from_db()
        assert self.watched_thread.category_id == category.id
