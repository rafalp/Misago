from django.db import models, transaction
from django.http import HttpRequest

from ...threads.checksums import update_post_checksum
from ...threads.models import Post, Thread
from ..hooks import (
    get_reply_private_thread_state_hook,
    get_reply_thread_state_hook,
    save_start_private_thread_state_hook,
    save_start_thread_state_hook,
)
from .base import PostingState


class ReplyThreadState(PostingState):
    # True if new reply was merged with the recent post
    is_merged: bool

    def __init__(self, request: HttpRequest, thread: Thread, post: Post | None = None):
        super().__init__(request)

        self.category = thread.category
        self.thread = thread
        self.post = post or self.initialize_post()
        self.is_merged = bool(self.post.id)

        self.store_object_state(self.category)
        self.store_object_state(self.thread)

        if self.post.id:
            self.store_object_state(self.post)

    def set_post_message(self, message: str):
        if self.post.id:
            message = "\n\n".join([self.post.original, message])

        super().set_post_message(message)

    @transaction.atomic()
    def save(self):
        save_start_thread_state_hook(self.save_action, self.request, self)

    def save_action(self, request: HttpRequest, state: "ReplyThreadState"):
        self.save_post()
        self.save_attachments()

        self.save_thread()

        self.save_category()
        self.save_user()

    def save_post(self):
        if self.post.id:
            self.post.updated_on = self.timestamp
            self.post.edits = models.F("edits") + 1
            self.post.last_editor = self.user
            self.post.last_editor_name = self.user.username
            self.post.last_editor_slug = self.user.slug
        else:
            # Save new post so it exists before search vector setup
            self.post.save()

        update_post_checksum(self.post)
        self.post.update_search_vector()
        self.post.save()

    def save_thread(self):
        if not self.is_merged:
            self.thread.replies = models.F("replies") + 1
            self.thread.set_last_post(self.post)

        self.update_object(self.thread)

    def save_category(self):
        if not self.is_merged:
            self.category.posts = models.F("posts") + 1
            self.category.set_last_thread(self.thread)

        self.update_object(self.category)

    def save_user(self):
        if not self.is_merged:
            self.user.posts = models.F("posts") + 1
            self.user.last_posted_on = self.timestamp

        self.update_object(self.user)


class ReplyPrivateThreadState(ReplyThreadState):
    @transaction.atomic()
    def save(self):
        save_start_private_thread_state_hook(self.save_action, self.request, self)


def get_reply_thread_state(
    request: HttpRequest, thread: Thread, post: Post | None = None
) -> ReplyThreadState:
    return get_reply_thread_state_hook(
        _get_reply_thread_state_action, request, thread, post
    )


def _get_reply_thread_state_action(
    request: HttpRequest, thread: Thread, post: Post | None = None
) -> ReplyThreadState:
    return ReplyThreadState(request, thread, post)


def get_reply_private_thread_state(
    request: HttpRequest, thread: Thread, post: Post | None = None
) -> ReplyPrivateThreadState:
    return get_reply_private_thread_state_hook(
        _get_reply_private_thread_state_action, request, thread, post
    )


def _get_reply_private_thread_state_action(
    request: HttpRequest, thread: Thread, post: Post | None = None
) -> ReplyPrivateThreadState:
    return ReplyPrivateThreadState(request, thread, post)
