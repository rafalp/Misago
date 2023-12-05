from django.db import models
from django.utils.translation import pgettext_lazy

from ...plugins.models import PluginDataModel


class AttachmentType(PluginDataModel):
    ENABLED = 0
    LOCKED = 1
    DISABLED = 2

    name = models.CharField(max_length=255)
    extensions = models.CharField(max_length=255)
    mimetypes = models.CharField(null=True, blank=True, max_length=255)
    size_limit = models.PositiveIntegerField(default=1024)
    status = models.PositiveIntegerField(
        default=ENABLED,
        choices=[
            (
                ENABLED,
                pgettext_lazy(
                    "attachment availability choice",
                    "Allow uploads and downloads",
                ),
            ),
            (
                LOCKED,
                pgettext_lazy(
                    "attachment availability choice",
                    "Allow downloads only",
                ),
            ),
            (
                DISABLED,
                pgettext_lazy(
                    "attachment availability choice",
                    "Disallow both uploading and downloading",
                ),
            ),
        ],
    )

    limit_uploads_to = models.ManyToManyField(
        "misago_acl.Role", related_name="+", blank=True
    )
    limit_downloads_to = models.ManyToManyField(
        "misago_acl.Role", related_name="+", blank=True
    )

    def __str__(self):
        return self.name

    @property
    def is_enabled(self):
        return self.status == AttachmentType.ENABLED

    @property
    def is_locked(self):
        return self.status == AttachmentType.LOCKED

    @property
    def extensions_list(self):
        if self.extensions:
            return self.extensions.split(",")
        return []

    @property
    def mimetypes_list(self):
        if self.mimetypes:
            return self.mimetypes.split(",")
        return []
