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

if TYPE_CHECKING:
    from ...threads.models import Thread


class Post(PluginDataModel):
    category = models.ForeignKey("misago_categories.Category", on_delete=models.CASCADE)
    thread = models.ForeignKey("misago_threads.Thread", on_delete=models.CASCADE)
    poster = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL
    )
    poster_name = models.CharField(max_length=255)

    original = models.TextField()
    parsed = models.TextField()
    metadata = models.JSONField(default=dict)

    posted_at = models.DateTimeField(db_index=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    hidden_at = models.DateTimeField(null=True, blank=True)

    edits = models.PositiveIntegerField(default=0)
    last_editor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    last_editor_name = models.CharField(max_length=255, null=True, blank=True)
    last_editor_slug = models.SlugField(max_length=255, null=True, blank=True)

    hidden_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    hidden_by_name = models.CharField(max_length=255, null=True, blank=True)
    hidden_by_slug = models.SlugField(max_length=255, null=True, blank=True)

    has_reports = models.BooleanField(default=False)
    has_open_reports = models.BooleanField(default=False)

    is_unapproved = models.BooleanField(default=False, db_index=True)
    is_hidden = models.BooleanField(default=False)
    is_protected = models.BooleanField(default=False)

    search_document = models.TextField(null=True, blank=True)
    search_vector = SearchVectorField()

    class Meta:
        indexes = [
            *PluginDataModel.Meta.indexes,
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
            GinIndex(fields=["search_vector"]),
            # Speed up threadview for team members
            models.Index(fields=["thread", "id"]),
            models.Index(fields=["poster", "posted_at"]),
        ]

    def __str__(self):
        return "%s..." % self.original[10:].strip()

    @property
    def sha256_checksum(self) -> str:
        return hashlib.sha256(
            f"{self.id}:{self.updated_at or "n"}:{self.parsed}".encode()
        ).hexdigest()

    def set_search_document(self, thread: "Thread", search_document: str):
        if self.id == thread.first_post_id:
            self.search_document = f"{thread.title}\n\n{search_document}"
        else:
            self.search_document = search_document

    def set_search_vector(self):
        self.search_vector = SearchVector(
            "search_document", config=settings.MISAGO_SEARCH_CONFIG
        )

    def get_absolute_url(self):
        return reverse("misago:post", kwargs={"post_id": self.id})
