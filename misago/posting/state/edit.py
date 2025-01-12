from django.db import models, transaction
from django.http import HttpRequest

from ...threads.checksums import update_post_checksum
from ...threads.models import Post
from ..hooks import (
    get_edit_private_thread_post_state_hook,
    get_edit_thread_post_state_hook,
    save_edit_private_thread_post_state_hook,
    save_edit_thread_post_state_hook,
)
from .base import PostingState


class EditThreadPostState(PostingState):
    # This state can actually edit both post and its thread's title
    thread_title: str
    post_original: str

    def __init__(self, request: HttpRequest, post: Post):
        super().__init__(request)

        self.category = post.category
        self.thread = post.thread
        self.post = post

        self.store_object_state(self.category)
        self.store_object_state(self.thread)
        self.store_object_state(post)

        self.thread_title = self.thread.title
        self.post_original = post.original

    @transaction.atomic()
    def save(self):
        save_edit_thread_post_state_hook(self.save_action, self.request, self)

    def save_action(self, request: HttpRequest, state: "EditThreadPostState"):
        if self.post_original != self.post.original:
            self.save_post()

        if self.thread_title != self.thread.title:
            self.save_thread()

            if self.category.last_thread_id == self.thread.id:
                self.save_category()

        self.save_attachments()

    def save_post(self):
        self.post.updated_on = self.timestamp
        self.post.edits = models.F("edits") + 1
        self.post.last_editor = self.user
        self.post.last_editor_name = self.user.username
        self.post.last_editor_slug = self.user.slug
        self.update_object(self.post)

        update_post_checksum(self.post)
        self.post.update_search_vector()
        self.update_object(self.post)

    def save_thread(self):
        self.update_object(self.thread)

    def save_category(self):
        self.category.last_thread_title = self.thread.title
        self.category.last_thread_slug = self.thread.slug
        self.update_object(self.category)


class EditPrivateThreadPostState(EditThreadPostState):
    @transaction.atomic()
    def save(self):
        save_edit_private_thread_post_state_hook(self.save_action, self.request, self)


def get_edit_thread_post_state(request: HttpRequest, post: Post) -> EditThreadPostState:
    return get_edit_thread_post_state_hook(
        _get_edit_thread_post_state_action, request, post
    )


def _get_edit_thread_post_state_action(
    request: HttpRequest, post: Post
) -> EditThreadPostState:
    return EditThreadPostState(request, post)


def get_edit_private_thread_post_state(
    request: HttpRequest, post: Post
) -> EditPrivateThreadPostState:
    return get_edit_private_thread_post_state_hook(
        _get_edit_private_thread_post_state_action, request, post
    )


def _get_edit_private_thread_post_state_action(
    request: HttpRequest, post: Post
) -> EditPrivateThreadPostState:
    return EditPrivateThreadPostState(request, post)
