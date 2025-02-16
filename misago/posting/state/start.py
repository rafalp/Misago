from typing import TYPE_CHECKING

from django.db import models, transaction
from django.http import HttpRequest

from ...categories.models import Category
from ...core.utils import slugify
from ...threads.checksums import update_post_checksum
from ...threads.models import ThreadParticipant
from ..hooks import (
    get_start_private_thread_state_hook,
    get_start_thread_state_hook,
    save_start_private_thread_state_hook,
    save_start_thread_state_hook,
)
from .base import PostingState

if TYPE_CHECKING:
    from ...users.models import User


class StartThreadState(PostingState):
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

        save_start_thread_state_hook(self.save_action, self.request, self)

    def save_action(self, request: HttpRequest, state: "StartThreadState"):
        self.save_thread()
        self.save_post()
        self.save_attachments()

        self.save_category()
        self.save_user()

    def save_thread(self):
        self.thread.first_post = self.thread.last_post = self.post
        self.thread.save()

    def save_post(self):
        update_post_checksum(self.post)
        self.post.update_search_vector()
        self.post.save()

    def save_category(self):
        self.category.threads = models.F("threads") + 1
        self.category.posts = models.F("posts") + 1
        self.category.set_last_thread(self.thread)

        self.update_object(self.category)

    def save_user(self):
        self.user.threads = models.F("threads") + 1
        self.user.posts = models.F("posts") + 1
        self.user.last_posted_on = self.timestamp

        self.update_object(self.user)


class StartPrivateThreadState(StartThreadState):
    invite_users: list["User"]

    def __init__(self, request: HttpRequest, category: Category):
        super().__init__(request, category)
        self.invite_users: list["User"] = []

    def set_invite_users(self, users: list["User"]):
        self.invite_users = users

    @transaction.atomic()
    def save(self):
        self.thread.save()
        self.post.save()

        save_start_private_thread_state_hook(self.save_action, self.request, self)

    def save_action(self, request: HttpRequest, state: "StartPrivateThreadState"):
        super().save_action(request, state)

        self.save_users()

    def save_users(self):
        users: list[ThreadParticipant] = [
            ThreadParticipant(thread=self.thread, user=self.user, is_owner=True),
        ]

        for invite_user in self.invite_users:
            users.append(
                ThreadParticipant(thread=self.thread, user=invite_user),
            )

        ThreadParticipant.objects.bulk_create(users)


def get_start_thread_state(
    request: HttpRequest, category: Category
) -> StartThreadState:
    return get_start_thread_state_hook(
        _get_start_thread_state_action, request, category
    )


def _get_start_thread_state_action(
    request: HttpRequest, category: Category
) -> StartThreadState:
    return StartThreadState(request, category)


def get_start_private_thread_state(
    request: HttpRequest, category: Category
) -> StartPrivateThreadState:
    return get_start_private_thread_state_hook(
        _get_start_private_thread_state_action, request, category
    )


def _get_start_private_thread_state_action(
    request: HttpRequest, category: Category
) -> StartPrivateThreadState:
    return StartPrivateThreadState(request, category)
