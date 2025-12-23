from django.db import models, transaction
from django.http import HttpRequest

from ...edits.create import create_post_edit
from ...parser.parse import ParsingResult, parse
from ...threads.models import Post, Thread
from ..hooks import (
    get_private_thread_reply_state_hook,
    get_thread_reply_state_hook,
    save_private_thread_reply_state_hook,
    save_thread_reply_state_hook,
)
from .state import State


class ReplyState(State):
    # True if new reply was merged with the recent post
    is_merged: bool
    post_original: str

    def __init__(self, request: HttpRequest, thread: Thread, post: Post | None = None):
        super().__init__(request)

        self.category = thread.category
        self.thread = thread
        self.post = post or self.initialize_post()
        self.is_merged = bool(self.post.id)
        self.post_original = self.post.original

        self.store_object_state(self.category)
        self.store_object_state(self.thread)

        if self.post.id:
            self.store_object_state(self.post)

    def set_post_message(self, parsing_result: ParsingResult):
        if self.post.id:
            markup = "\n\n".join([self.post.original, parsing_result.markup])
            parsing_result = parse(markup)

        super().set_post_message(parsing_result)

    @transaction.atomic()
    def save(self):
        self.save_action(self.request, self)

    def save_action(self, request: HttpRequest, state: "ReplyState"):
        self.save_post()
        self.save_attachments()

        self.save_thread()

        self.save_category()
        self.save_user()

    def save_post(self):
        self.post.set_search_document(self.thread, self.parsing_result.text)

        post_edits = self.post.edits

        if self.post.id:
            self.post.updated_at = self.timestamp
            self.post.edits = models.F("edits") + 1
            self.post.last_editor = self.user
            self.post.last_editor_name = self.user.username
            self.post.last_editor_slug = self.user.slug
            self.post.last_edit_reason = None
            post_edits += 1

            create_post_edit(
                post=self.post,
                user=self.user,
                old_content=self.post_original,
                new_content=self.post.original,
                attachments=self.attachments,
                edited_at=self.timestamp,
                request=self.request,
            )
        else:
            # Save new post so it exists before search vector setup
            self.post.save()

        self.post.set_search_vector()
        self.post.save()

        # Replace edits attr with integer
        # Prevents HTMX merge reply from breaking
        self.post.edits = post_edits

        self.schedule_post_content_upgrade()

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
            self.user.last_posted_at = self.timestamp

        self.update_object(self.user)


class ThreadReplyState(ReplyState):
    @transaction.atomic()
    def save(self):
        save_thread_reply_state_hook(self.save_action, self.request, self)


class PrivateThreadReplyState(ReplyState):
    @transaction.atomic()
    def save(self):
        save_private_thread_reply_state_hook(self.save_action, self.request, self)


def get_reply_thread_state(
    request: HttpRequest, thread: Thread, post: Post | None = None
) -> ReplyState:
    return get_thread_reply_state_hook(
        _get_reply_thread_state_action, request, thread, post
    )


def _get_reply_thread_state_action(
    request: HttpRequest, thread: Thread, post: Post | None = None
) -> ReplyState:
    return ReplyState(request, thread, post)


def get_reply_private_thread_state(
    request: HttpRequest, thread: Thread, post: Post | None = None
) -> PrivateThreadReplyState:
    return get_private_thread_reply_state_hook(
        _get_reply_private_thread_state_action, request, thread, post
    )


def _get_reply_private_thread_state_action(
    request: HttpRequest, thread: Thread, post: Post | None = None
) -> PrivateThreadReplyState:
    return PrivateThreadReplyState(request, thread, post)
