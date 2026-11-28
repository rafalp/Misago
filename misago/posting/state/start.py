from typing import TYPE_CHECKING

from django.db import models, transaction
from django.http import HttpRequest

from ...categories.models import Category
from ...plugins import extensions
from ...polls.models import Poll
from ...privatethreads.models import PrivateThreadMember
from ...search.threads import threads_search
from ...threads.checksums import update_post_checksum
from ..approval import (
    require_private_thread_approval,
    require_thread_approval,
)
from .base import State

if TYPE_CHECKING:
    from ...users.models import User


class StartState(State):
    def __init__(self, request: HttpRequest, category: Category):
        super().__init__(request)

        self.category = category
        self.thread = self.initialize_thread()
        self.post = self.initialize_post()

        self.store_object_state(category)

    def require_approval(self) -> bool:
        return False

    @transaction.atomic
    def save_atomic(self):
        self.save()

    def save(self):
        self.thread.save()
        self.post.save()

        self.save_thread()
        self.save_post()
        self.save_attachments()
        self.save_search_index()

        self.save_category()
        self.save_user()

    def save_thread(self):
        self.thread.first_post = self.thread.last_post = self.post
        self.thread.is_unapproved = self.require_approval()
        self.thread.save()

    def save_post(self):
        update_post_checksum(self.post)
        self.schedule_post_content_upgrade()

    def save_search_index(self):
        self.index_thread()
        self.index_post()

    def save_category(self):
        if self.thread.is_unapproved:
            self.category.unapproved_threads = models.F("unapproved_threads") + 1
        else:
            self.category.threads = models.F("threads") + 1
            self.category.posts = models.F("posts") + 1
            self.category.set_last_thread(self.thread)

        self.update_object(self.category)

    def save_user(self):
        self.user.threads = models.F("threads") + 1
        self.user.posts = models.F("posts") + 1
        self.user.last_posted_at = self.timestamp

        self.update_object(self.user)


class ThreadStartState(StartState):
    poll: Poll | None

    def __init__(self, request: HttpRequest, category: Category):
        super().__init__(request, category)

        self.poll = None

    def set_poll(self, poll: Poll):
        self.poll = poll
        self.thread.has_poll = True

    def require_approval(self) -> bool:
        return require_thread_approval(self)

    def save(self):
        super().save()

        if self.poll:
            self.save_poll()

    def save_poll(self):
        self.poll.save()


class PrivateThreadStartState(StartState):
    members: list["User"]

    def __init__(self, request: HttpRequest, category: Category):
        super().__init__(request, category)

        self.members: list["User"] = []

    def set_members(self, users: list["User"]):
        self.members = users

    def require_approval(self) -> bool:
        return require_private_thread_approval(self)

    def save(self):
        super().save()

        self.save_members()

    def save_members(self):
        users: list[PrivateThreadMember] = [
            PrivateThreadMember(
                thread=self.thread,
                user=self.user,
                is_owner=True,
                created_at=self.timestamp,
            ),
        ]

        for user in self.members:
            users.append(
                PrivateThreadMember(
                    thread=self.thread,
                    user=user,
                    created_at=self.timestamp,
                ),
            )

        PrivateThreadMember.objects.bulk_create(users)

    def save_search_index(self):
        super().save_search_index()

        threads_search.update_thread_members(
            self.thread, [user.id for user in self.members]
        )
