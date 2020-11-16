from django.db import models


class Icon(models.Model):
    TYPE_FAVICON = "favicon"
    TYPE_FAVICON_32 = "favicon_32"
    TYPE_FAVICON_16 = "favicon_16"

    TYPE_APPLE_TOUCH_ICON = "apple_touch_icon"

    FAVICON_TYPES = (TYPE_FAVICON, TYPE_FAVICON_32, TYPE_FAVICON_16)

    type = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to="icon", height_field="height", width_field="width"
    )
    size = models.PositiveIntegerField(default=0)
    width = models.PositiveIntegerField(default=0)
    height = models.PositiveIntegerField(default=0)

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete(save=False)
        return super().delete(*args, **kwargs)
