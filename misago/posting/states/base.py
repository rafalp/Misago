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


class State:
    request: HttpRequest
    timestamp: datetime
    user: "User"

    category: Category
    thread: Thread
    post: Post

    parser_context: ParserContext
    message_ast: list[dict] | None
    message_metadata: dict | None

    models_states: dict

    def __init__(self, request: HttpRequest):
        self.request = request
        self.timestamp = timezone.now()
        self.user = request.user

        self.parser_context = self.initialize_parser_context()
        self.message_ast = None
        self.message_metadata = None

        self.models_states = {}
        self.store_model_state(self.user)

    def store_model_state(self, model: models.Model):
        state_key = self.get_model_state_key(model)
        self.models_states[state_key] = self.get_model_state(model)

    def get_model_state_key(self, model: models.Model) -> str:
        return f"{model.__class__.__name__}:{model.pk}"

    def get_model_state(self, model: models.Model) -> dict[str, Any]:
        state = {}

        for field in model._meta.get_fields():
            if not isinstance(
                field,
                (models.ManyToManyRel, models.ManyToOneRel, models.ManyToManyField),
            ):
                state[field.name] = deepcopy(getattr(model, field.attname))

        return state

    def get_model_changed_fields(self, model: models.Model) -> set[str]:
        state_key = self.get_model_state_key(model)
        old_state = self.models_states[state_key]

        changed_fields: set[str] = set()
        for field, value in self.get_model_state(model).items():
            if old_state[field] != value:
                changed_fields.add(field)

        return changed_fields

    def save_model_changes(self, model: models.Model) -> set[str]:
        update_fields = self.get_model_changed_fields(model)
        if update_fields:
            model.save(update_fields=update_fields)
        return update_fields

    def initialize_parser_context(self) -> ParserContext:
        return create_parser_context(self.request, content_type=ContentType.POST)

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
