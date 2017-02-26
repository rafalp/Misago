from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class AttachmentType(models.Model):
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
            (ENABLED, _("Allow uploads and downloads")),
            (LOCKED, _("Allow downloads only")),
            (DISABLED, _("Disallow both uploading and downloading")),
        ],
    )

    limit_uploads_to = models.ManyToManyField('misago_acl.Role', related_name='+', blank=True)
    limit_downloads_to = models.ManyToManyField('misago_acl.Role', related_name='+', blank=True)

    def __str__(self):
        return self.name

    @property
    def is_enabled(self):
        return self.status == AttachmentType.ENABLED

    @property
    def extensions_list(self):
        if self.extensions:
            return self.extensions.split(',')
        return []

    @property
    def mimetypes_list(self):
        if self.mimetypes:
            return self.mimetypes.split(',')
        return []
