from copy import deepcopy
from datetime import datetime
from typing import Any, TYPE_CHECKING

from django.db import models
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
from ...threads.models import Post, Thread

if TYPE_CHECKING:
    from ...users.models import User


class PostingState:
    request: HttpRequest
    timestamp: datetime
    user: "User"

    category: Category
    thread: Thread
    post: Post

    parser_context: ParserContext
    message_ast: list[dict] | None
    message_metadata: dict | None

    state: dict
    plugin_state: dict

    def __init__(self, request: HttpRequest):
        self.request = request
        self.timestamp = timezone.now()
        self.user = request.user

        self.parser_context = self.initialize_parser_context()
        self.message_ast = None
        self.message_metadata = None

        self.state = {}
        self.plugin_state = {}

        self.store_object_state(self.user)

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

    def store_object_state(self, obj: models.Model):
        state_key = self.get_object_state_key(obj)
        self.state[state_key] = self.get_object_state(obj)

    def get_object_state_key(self, obj: models.Model) -> str:
        return f"{obj.__class__.__name__}:{obj.pk}"

    def get_object_state(self, obj: models.Model) -> dict[str, Any]:
        state = {}

        for field in obj._meta.get_fields():
            if not isinstance(
                field,
                (models.ManyToManyRel, models.ManyToOneRel, models.ManyToManyField),
            ):
                state[field.name] = deepcopy(getattr(obj, field.attname))

        return state

    def get_object_changed_fields(self, obj: models.Model) -> set[str]:
        state_key = self.get_object_state_key(obj)
        old_state = self.state[state_key]

        changed_fields: set[str] = set()
        for field, value in self.get_object_state(obj).items():
            if old_state[field] != value:
                changed_fields.add(field)

        return changed_fields

    def update_object(self, obj: models.Model) -> set[str]:
        update_fields = self.get_object_changed_fields(obj)
        if update_fields:
            obj.save(update_fields=update_fields)
        self.store_object_state(obj)
        return update_fields

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
