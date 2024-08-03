from datetime import datetime
from typing import TYPE_CHECKING

from django.db import models, transaction
from django.http import HttpRequest
from django.utils import timezone

from ...categories.models import Category
from ...core.utils import slugify
from ...parser.context import ParserContext, create_parser_context
from ...parser.enums import ContentType, PlainTextFormat
from ...parser.factory import create_parser
from ...parser.html import render_ast_to_html
from ...parser.metadata import create_ast_metadata
from ...parser.plaintext import render_ast_to_plaintext
from ...threads.checksums import update_post_checksum
from ...threads.models import Post, Thread

if TYPE_CHECKING:
    from ...users.models import User


class StartState:
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
        self.request = request
        self.timestamp = timezone.now()
        self.category = category
        self.user = request.user

        self.thread = self.initialize_thread()
        self.post = self.initialize_post()

        self.parser_context = self.initialize_parser_context()

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

    def initialize_parser_context(self) -> ParserContext:
        return create_parser_context(self.request, content_type=ContentType.POST)

    def set_thread_title(self, title: str):
        self.thread.title = title
        self.thread.slug = slugify(title)

    def set_post_message(self, message: str):
        parser = create_parser(self.parser_context)
        ast = parser(message)
        metadata = create_ast_metadata(self.parser_context, ast)

        self.post.original = message
        self.post.parsed = render_ast_to_html(self.parser_context, ast, metadata)
        self.post.search_document = render_ast_to_plaintext(
            self.parser_context,
            ast,
            metadata,
            text_format=PlainTextFormat.SEARCH_DOCUMENT,
        )

        self.message_ast = ast
        self.message_metadata = metadata

    @transaction.atomic()
    def save(self):
        self.thread.save()
        self.post.save()

        self.save_final_thread()
        self.save_final_post()

        self.save_category()
        self.save_user()

    def save_final_thread(self):
        self.thread.first_post = self.thread.last_post = self.post
        self.thread.save()

    def save_final_post(self):
        update_post_checksum(self.post)
        self.post.update_search_vector()
        self.post.save()

    def save_category(self):
        self.category.threads = models.F("threads") + 1
        self.category.posts = models.F("posts") + 1
        self.category.set_last_thread(self.thread)
        self.category.save()

    def save_user(self):
        self.user.threads = models.F("threads") + 1
        self.user.posts = models.F("posts") + 1
        self.user.save()


class StartThreadState(StartState):
    pass
