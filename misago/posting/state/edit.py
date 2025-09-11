from django.db import models, transaction
from django.http import HttpRequest

from ...posts.models import Post
from ...threadupdates.create import create_changed_title_thread_update
from ...threadupdates.models import ThreadUpdate
from ..hooks import (
    get_private_thread_post_edit_state_hook,
    get_thread_post_edit_state_hook,
    save_private_thread_post_edit_state_hook,
    save_thread_post_edit_state_hook,
)
from .state import State


class PostEditState(State):
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
        self.save_action(self.request, self)

    def save_action(self, request: HttpRequest, state: "PostEditState"):
        if self.post_original != self.post.original:
            self.save_post()

        if self.thread_title != self.thread.title:
            self.save_thread()

            if self.category.last_thread_id == self.thread.id:
                self.save_category()

            create_changed_title_thread_update(
                self.thread, self.thread_title, request.user, request
            )

            ThreadUpdate.objects.context_object(self.thread).update(
                context=self.thread.title
            )

        self.save_attachments()

    def save_post(self):
        self.post.set_search_document(self.thread, self.parsing_result.text)
        self.post.updated_at = self.timestamp
        self.post.edits = models.F("edits") + 1
        self.post.last_editor = self.user
        self.post.last_editor_name = self.user.username
        self.post.last_editor_slug = self.user.slug
        self.update_object(self.post)

        self.post.set_search_vector()
        self.update_object(self.post)

        self.schedule_post_content_upgrade()

    def save_thread(self):
        self.update_object(self.thread)

    def save_category(self):
        self.category.last_thread_title = self.thread.title
        self.category.last_thread_slug = self.thread.slug
        self.update_object(self.category)


class ThreadPostEditState(PostEditState):
    @transaction.atomic()
    def save(self):
        save_thread_post_edit_state_hook(self.save_action, self.request, self)


class PrivateThreadPostEditState(PostEditState):
    @transaction.atomic()
    def save(self):
        save_private_thread_post_edit_state_hook(self.save_action, self.request, self)


def get_thread_post_edit_state(request: HttpRequest, post: Post) -> ThreadPostEditState:
    return get_thread_post_edit_state_hook(
        _get_thread_post_edit_state_action, request, post
    )


def _get_thread_post_edit_state_action(
    request: HttpRequest, post: Post
) -> ThreadPostEditState:
    return ThreadPostEditState(request, post)


def get_private_thread_post_edit_state(
    request: HttpRequest, post: Post
) -> PrivateThreadPostEditState:
    return get_private_thread_post_edit_state_hook(
        _get_private_thread_post_edit_state_action, request, post
    )


def _get_private_thread_post_edit_state_action(
    request: HttpRequest, post: Post
) -> PrivateThreadPostEditState:
    return PrivateThreadPostEditState(request, post)
