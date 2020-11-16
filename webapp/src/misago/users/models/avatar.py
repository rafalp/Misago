from django.conf import settings
from django.db import models

from ..avatars import store


class Avatar(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    size = models.PositiveIntegerField(default=0)
    image = models.ImageField(max_length=255, upload_to=store.upload_to)

    @property
    def url(self):
        return self.image.url
