from django.db import models

class WarnLevel(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(null=True, blank=True)
    warning_level = models.PositiveIntegerField(default=1, db_index=True)
    expires_after_minutes = models.PositiveIntegerField(default=0)
    inhibit_posting_threads = models.PositiveIntegerField(default=0)
    inhibit_posting_replies = models.PositiveIntegerField(default=0)

    class Meta:
        app_label = 'misago'
