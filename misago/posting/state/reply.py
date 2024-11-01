from django.db import models, transaction
from django.http import HttpRequest

from ...threads.checksums import update_post_checksum
from ...threads.models import Thread
from ..hooks import (
    get_reply_private_thread_state_hook,
    get_reply_thread_state_hook,
    save_start_private_thread_state_hook,
    save_start_thread_state_hook,
)
from .base import PostingState


class ReplyThreadState(PostingState):
    def __init__(self, request: HttpRequest, thread: Thread):
        super().__init__(request)

        self.category = thread.category
        self.thread = thread
        self.post = self.initialize_post()

        self.store_object_state(self.category)
        self.store_object_state(self.thread)

    @transaction.atomic()
    def save(self):
        save_start_thread_state_hook(self.save_action, self.request, self)

    def save_action(self, request: HttpRequest, state: "ReplyThreadState"):
        self.save_post()
        self.save_thread()

        self.save_category()
        self.save_user()

    def save_thread(self):
        self.thread.replies = models.F("replies") + 1
        self.thread.set_last_post(self.post)

        self.update_object(self.thread)

    def save_post(self):
        self.post.save()

        update_post_checksum(self.post)
        self.post.update_search_vector()
        self.post.save()

    def save_category(self):
        self.category.posts = models.F("posts") + 1
        self.category.set_last_thread(self.thread)

        self.update_object(self.category)

    def save_user(self):
        self.user.posts = models.F("posts") + 1

        self.update_object(self.user)


class ReplyPrivateThreadState(ReplyThreadState):
    @transaction.atomic()
    def save(self):
        save_start_private_thread_state_hook(self.save_action, self.request, self)


def get_reply_thread_state(request: HttpRequest, thread: Thread) -> ReplyThreadState:
    return get_reply_thread_state_hook(_get_reply_thread_state_action, request, thread)


def _get_reply_thread_state_action(
    request: HttpRequest, thread: Thread
) -> ReplyThreadState:
    return ReplyThreadState(request, thread)


def get_reply_private_thread_state(
    request: HttpRequest, thread: Thread
) -> ReplyPrivateThreadState:
    return get_reply_private_thread_state_hook(
        _get_reply_private_thread_state_action, request, thread
    )


def _get_reply_private_thread_state_action(
    request: HttpRequest, thread: Thread
) -> ReplyPrivateThreadState:
    return ReplyPrivateThreadState(request, thread)
