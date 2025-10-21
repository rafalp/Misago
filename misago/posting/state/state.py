from copy import deepcopy
from datetime import datetime
from typing import Any, TYPE_CHECKING

from django.db import models
from django.http import HttpRequest
from django.utils import timezone

from ...attachments.delete import delete_attachments
from ...attachments.models import Attachment
from ...categories.models import Category
from ...core.utils import slugify
from ...parser.parse import ParsingResult
from ...threads.models import Post, Thread
from ..tasks import upgrade_post_content
from ..upgradepost import post_needs_content_upgrade

if TYPE_CHECKING:
    from ...users.models import User


class State:
    request: HttpRequest
    timestamp: datetime
    user: "User"

    category: Category
    thread: Thread
    post: Post
    parsing_result: ParsingResult
    attachments: list[Attachment]
    delete_attachments: list[Attachment]

    state: dict
    plugin_state: dict

    def __init__(self, request: HttpRequest):
        self.request = request
        self.timestamp = timezone.now()
        self.user = request.user

        self.state = {}
        self.plugin_state = {}

        self.parsing_result = None
        self.attachments = []
        self.delete_attachments = []

        self.store_object_state(self.user)

    def initialize_thread(self) -> Thread:
        return Thread(
            category=self.category,
            started_at=self.timestamp,
            last_posted_at=self.timestamp,
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
            posted_at=self.timestamp,
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

    def set_thread_title(self, title: str):
        self.thread.title = title
        self.thread.slug = slugify(title)

    def set_post_message(self, parsing_result: ParsingResult):
        self.parsing_result = parsing_result

        self.post.original = parsing_result.markup
        self.post.parsed = parsing_result.html
        self.post.metadata = parsing_result.metadata

    def schedule_post_content_upgrade(self):
        if post_needs_content_upgrade(self.post):
            upgrade_post_content.delay(self.post.id, self.post.sha256_checksum)

    def set_attachments(self, attachments: list[Attachment]):
        self.attachments = attachments

    def set_delete_attachments(self, attachments: list[Attachment]):
        self.delete_attachments = []
        delete_ids: set[int] = set(a.id for a in attachments)
        save_attachments: list[Attachment] = []

        for attachment in self.attachments:
            if attachment.id in delete_ids:
                self.delete_attachments.append(attachment)
            else:
                save_attachments.append(attachment)

        self.set_attachments(save_attachments)

    def save_attachments(self):
        for attachment in self.attachments:
            if attachment.post_id:
                continue

            attachment.associate_with_post(self.post)
            attachment.uploaded_at = self.timestamp
            attachment.save()

        if self.delete_attachments:
            delete_attachments(self.delete_attachments, request=self.request)
