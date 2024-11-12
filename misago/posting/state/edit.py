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
    def __init__(self, request: HttpRequest, post: Post):
        super().__init__(request)

        self.category = post.category
        self.thread = post.thread
        self.post = post

        self.store_object_state(self.category)
        self.store_object_state(self.thread)
        self.store_object_state(post)

    @transaction.atomic()
    def save(self):
        save_edit_thread_post_state_hook(self.save_action, self.request, self)

    def save_action(self, request: HttpRequest, state: "EditThreadPostState"):
        self.save_post()

    def save_post(self):
        self.post.edits = models.F("edits") + 1
        self.post.last_editor = self.user
        self.post.last_editor_name = self.user.username
        self.post.last_editor_slug = self.user.slug
        self.post.save()

        update_post_checksum(self.post)
        self.post.update_search_vector()
        self.post.save()


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
