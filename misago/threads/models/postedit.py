import difflib

from django.conf import settings
from django.db import models
from django.utils import timezone


class PostEdit(models.Model):
    category = models.ForeignKey('misago_categories.Category', on_delete=models.CASCADE)
    thread = models.ForeignKey('misago_threads.Thread', on_delete=models.CASCADE)
    post = models.ForeignKey(
        'misago_threads.Post',
        related_name='edits_record',
        on_delete=models.CASCADE,
    )

    edited_on = models.DateTimeField(default=timezone.now)

    editor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    editor_name = models.CharField(max_length=255)
    editor_slug = models.CharField(max_length=255)
    editor_ip = models.GenericIPAddressField()

    edited_from = models.TextField()
    edited_to = models.TextField()

    class Meta:
        ordering = ['-id']

    def get_diff(self):
        return difflib.ndiff(self.edited_from.splitlines(), self.edited_to.splitlines())
