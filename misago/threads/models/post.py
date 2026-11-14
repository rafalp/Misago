import copy
import hashlib
from typing import TYPE_CHECKING

from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.db import models
from django.db.models import Q
from django.urls import reverse

from ...conf import settings
from ...core.utils import parse_iso8601_string
from ...plugins.models import PluginDataModel
from ..checksums import is_post_valid, update_post_checksum

if TYPE_CHECKING:
    from .thread import Thread


class Post(PluginDataModel):
    category = models.ForeignKey("misago_categories.Category", on_delete=models.CASCADE)
    thread = models.ForeignKey("misago_threads.Thread", on_delete=models.CASCADE)
    poster = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    poster_name = models.CharField(max_length=255)

    content = models.TextField()
    content_parsed = models.TextField()
    checksum = models.CharField(max_length=64, default="-")
    metadata = models.JSONField(default=dict)

    attachments_cache = models.JSONField(null=True, blank=True)

    posted_at = models.DateTimeField(db_index=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    edits = models.PositiveIntegerField(default=0)
    last_editor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    last_editor_name = models.CharField(max_length=255, null=True, blank=True)
    last_editor_slug = models.CharField(max_length=255, null=True, blank=True)
    last_edit_reason = models.CharField(max_length=255, null=True, blank=True)

    is_locked = models.BooleanField(default=False)
    locked_at = models.DateTimeField(null=True, blank=True)
    locked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="+",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    locked_by_name = models.CharField(max_length=255, null=True, blank=True)
    locked_by_slug = models.CharField(max_length=255, null=True, blank=True)
    lock_reason = models.CharField(max_length=255, null=True, blank=True)

    is_hidden = models.BooleanField(default=False)
    hidden_at = models.DateTimeField(null=True, blank=True)
    hidden_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    hidden_by_name = models.CharField(max_length=255, null=True, blank=True)
    hidden_by_slug = models.CharField(max_length=255, null=True, blank=True)
    hide_reason = models.CharField(max_length=255, null=True, blank=True)

    has_reports = models.BooleanField(default=False)
    has_open_reports = models.BooleanField(default=False)
    is_unapproved = models.BooleanField(default=False, db_index=True)

    likes = models.PositiveIntegerField(default=0)
    last_likes = models.JSONField(null=True, blank=True)

    class Meta(PluginDataModel.Meta):
        indexes = PluginDataModel.Meta.indexes + [
            models.Index(
                name="misago_post_has_open_repo_part",
                fields=["has_open_reports"],
                condition=Q(has_open_reports=True),
            ),
            models.Index(
                name="misago_post_is_hidden_part",
                fields=["is_hidden"],
                condition=Q(is_hidden=False),
            ),
            # Speed up some views for team members
            models.Index(fields=["thread", "id"]),
            models.Index(fields=["poster", "posted_at"]),
        ]

    def __str__(self):
        return "%s..." % self.content[10:].strip()

    def delete(self, *args, **kwargs):
        from ..signals import delete_post

        delete_post.send(sender=self)

        super().delete(*args, **kwargs)

    @property
    def sha256_checksum(self) -> str:
        return hashlib.sha256(
            f"{self.id}:{self.updated_at or 0}:{self.content_parsed}".encode()
        ).hexdigest()

    @property
    def thread_type(self):
        return self.category.thread_type

    def get_absolute_url(self):
        return reverse("misago:post", kwargs={"post_id": self.id})

    def get_api_url(self):
        return self.thread_type.get_post_api_url(self)

    def get_likes_api_url(self):
        return self.thread_type.get_post_likes_api_url(self)

    def get_editor_api_url(self):
        return self.thread_type.get_post_editor_api_url(self)

    def get_edits_api_url(self):
        return self.thread_type.get_post_edits_api_url(self)

    @property
    def short(self):
        if self.is_valid:
            if len(self.original) > 150:
                return str("%s...") % self.original[:150].strip()
            return self.original
        return ""

    @property
    def is_valid(self):
        return is_post_valid(self)
