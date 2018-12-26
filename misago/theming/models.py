from django.db import models
from django.utils.translation import gettext
from mptt.models import MPTTModel, TreeForeignKey


class Theme(MPTTModel):
    parent = TreeForeignKey(
        "self", on_delete=models.PROTECT, null=True, blank=True, related_name="children"
    )
    name = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    version = models.CharField(max_length=255, null=True, blank=True)
    author = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(max_length=255, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ["is_default", "name"]

    def __str__(self):
        if self.is_default:
            return gettext("Default Misago Theme")
        return self.name

    @property
    def level_range(self):
        return range(self.level)


class Css(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.PROTECT, related_name="css")

    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255, null=True, blank=True)
    file = models.ImageField(max_length=255, null=True, blank=True)
    size = models.PositiveIntegerField()

    order = models.IntegerField(default=0)
    is_enabled = models.BooleanField(default=True)

    uploaded_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class Font(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.PROTECT, related_name="fonts")

    name = models.CharField(max_length=255)
    file = models.FileField(max_length=255)
    type = models.CharField(max_length=255)
    size = models.PositiveIntegerField()

    uploaded_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Image(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.PROTECT, related_name="images")

    name = models.CharField(max_length=255)
    file = models.ImageField(max_length=255)
    type = models.CharField(max_length=255)
    width = models.PositiveIntegerField()
    heigh = models.PositiveIntegerField()
    size = models.PositiveIntegerField()

    uploaded_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
