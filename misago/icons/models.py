from django.db import models


class Icon(models.Model):
    TYPE_FAVICON = ("favicon", "favicon_32", "favicon_16")
    TYPE_APPLE_TOUCH_ICON = "apple_touch_icon"

    type = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to="icon", height_field="height", width_field="width"
    )
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
