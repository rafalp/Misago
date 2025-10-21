from typing import TYPE_CHECKING

from django.db import models, transaction
from django.http import HttpRequest

from ...categories.models import Category
from ...polls.models import Poll
from ...privatethreads.models import PrivateThreadMember
from ...threads.checksums import update_post_checksum
from ..hooks import (
    get_private_thread_start_state_hook,
    get_thread_start_state_hook,
    save_private_thread_start_state_hook,
    save_thread_start_state_hook,
)
from .state import State

if TYPE_CHECKING:
    from ...users.models import User


class StartState(State):
    def __init__(self, request: HttpRequest, category: Category):
        super().__init__(request)

        self.category = category
        self.thread = self.initialize_thread()
        self.post = self.initialize_post()

        self.store_object_state(category)

    @transaction.atomic()
    def save(self):
        self.thread.save()
        self.post.save()

    def save_action(self, request: HttpRequest, state: "StartState"):
        self.save_thread()
        self.save_post()
        self.save_attachments()

        self.save_category()
        self.save_user()

    def save_thread(self):
        self.thread.first_post = self.thread.last_post = self.post
        self.thread.save()

    def save_post(self):
        self.post.set_search_document(self.thread, self.parsing_result.text)
        update_post_checksum(self.post)

        self.post.set_search_vector()
        self.post.save()

        self.schedule_post_content_upgrade()

    def save_category(self):
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

    @transaction.atomic()
    def save(self):
        super().save()

        save_thread_start_state_hook(self.save_action, self.request, self)

    def save_action(self, request: HttpRequest, state: "ThreadStartState"):
        super().save_action(request, state)

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

    @transaction.atomic()
    def save(self):
        super().save()

        save_private_thread_start_state_hook(self.save_action, self.request, self)

    def save_action(self, request: HttpRequest, state: "PrivateThreadStartState"):
        super().save_action(request, state)

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


def get_thread_start_state(
    request: HttpRequest, category: Category
) -> ThreadStartState:
    return get_thread_start_state_hook(
        _get_thread_start_state_action, request, category
    )


def _get_thread_start_state_action(
    request: HttpRequest, category: Category
) -> ThreadStartState:
    return ThreadStartState(request, category)


def get_private_thread_start_state(
    request: HttpRequest, category: Category
) -> PrivateThreadStartState:
    return get_private_thread_start_state_hook(
        _get_private_thread_start_state_action, request, category
    )


def _get_private_thread_start_state_action(
    request: HttpRequest, category: Category
) -> PrivateThreadStartState:
    return PrivateThreadStartState(request, category)
