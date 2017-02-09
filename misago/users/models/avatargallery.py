from django.db import models

from misago.users.avatars import store


class AvatarGallery(models.Model):
    gallery = models.CharField(max_length=255)
    image = models.ImageField(max_length=255, upload_to=store.upload_to)

    class Meta:
        ordering = ['gallery', 'pk']

    @property
    def path(self):
        return self.image.path

    @property
    def url(self):
        return self.image.url
