from datetime import datetime
from typing import TYPE_CHECKING

from django.db import models, transaction
from django.http import HttpRequest

from ...categories.models import Category
from ...core.utils import slugify
from ...parser.context import ParserContext
from ...threads.checksums import update_post_checksum
from ...threads.models import Post, Thread, ThreadParticipant
from .base import State

if TYPE_CHECKING:
    from ...users.models import User


class StartThreadState(State):
    request: HttpRequest
    timestamp: datetime
    category: Category
    thread: Thread
    post: Post
    user: "User"
    parser_context: ParserContext | None
    message_ast: list[dict] | None
    message_metadata: dict | None

    def __init__(self, request: HttpRequest, category: Category):
        super().__init__(request)

        self.category = category
        self.thread = self.initialize_thread()
        self.post = self.initialize_post()

        self.store_model_state(category)

    def initialize_thread(self) -> Thread:
        return Thread(
            category=self.category,
            started_on=self.timestamp,
            last_post_on=self.timestamp,
            starter=self.user,
            starter_name=self.user.username,
            starter_slug=self.user.slug,
            last_poster=self.user,
            last_poster_name=self.user.username,
            last_poster_slug=self.user.slug,
        )

    def initialize_post(self) -> Post:
        return Post(
            category=self.category,
            thread=self.thread,
            poster=self.user,
            poster_name=self.user.username,
            posted_on=self.timestamp,
            updated_on=self.timestamp,
        )

    def set_thread_title(self, title: str):
        self.thread.title = title
        self.thread.slug = slugify(title)

    @transaction.atomic()
    def save(self):
        self.thread.save()
        self.post.save()

        self.save_action()

    def save_action(self):
        self.save_thread()
        self.save_post()

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

        self.save_model_changes(self.category)

    def save_user(self):
        self.user.threads = models.F("threads") + 1
        self.user.posts = models.F("posts") + 1

        self.save_model_changes(self.user)


class StartPrivateThreadState(StartThreadState):
    invite_users: list["User"]

    def __init__(self, request: HttpRequest, category: Category):
        super().__init__(request, category)
        self.invite_users: list["User"] = []

    def set_invite_users(self, users: list["User"]):
        self.invite_users = users

    def save_action(self):
        super().save_action()

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
