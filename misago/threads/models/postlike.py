from django.conf import settings
from django.db import models
from django.utils import timezone


class PostLike(models.Model):
    category = models.ForeignKey('misago_categories.Category')
    thread = models.ForeignKey('misago_threads.Thread')
    post = models.ForeignKey('misago_threads.Post')

    liker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    liker_name = models.CharField(max_length=255, db_index=True)
    liker_slug = models.CharField(max_length=255)
    liker_ip = models.GenericIPAddressField()

    liked_on = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-id']
