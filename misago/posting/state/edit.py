from django.db import models, transaction
from django.http import HttpRequest

from ...edits.create import create_post_edit
from ...threads.models import Post
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
    edit_reason: str

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
        self.edit_reason = None

    def set_edit_reason(self, edit_reason: str):
        self.edit_reason = edit_reason

    def set_post_edits(self):
        self.post.updated_at = self.timestamp
        self.post.edits = models.F("edits") + 1
        self.post.last_editor = self.user
        self.post.last_editor_name = self.user.username
        self.post.last_editor_slug = self.user.slug
        self.post.last_edit_reason = self.edit_reason

    def is_post_changed(self):
        if self.thread_title != self.thread.title:
            return True

        if self.post_original != self.post.original:
            return True

        if self.delete_attachments:
            return True

        for attachment in self.attachments:
            if not attachment.post_id:
                return True

        return False

    @transaction.atomic()
    def save(self):
        self.save_action(self.request, self)

    def save_action(self, request: HttpRequest, state: "PostEditState"):
        if self.is_post_changed():
            post_edits = self.post.edits + 1

            self.set_post_edits()
            if self.post_original != self.post.original:
                # Full post update
                self.save_post()
            else:
                self.update_object(self.post)

            create_post_edit(
                post=self.post,
                user=self.user,
                edit_reason=self.edit_reason,
                old_title=self.thread_title,
                new_title=self.thread.title,
                old_content=self.post_original,
                new_content=self.post.original,
                attachments=self.attachments,
                deleted_attachments=self.delete_attachments,
                edited_at=self.timestamp,
                request=self.request,
            )

            # Replace edits attr with integer
            # Prevents inline HTMX edit from breaking
            self.post.edits = post_edits + 1

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
