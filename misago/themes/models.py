from django.db import models
from django.utils.translation import gettext
from mptt.models import MPTTModel, TreeForeignKey

from .uploadto import (
    generate_theme_dirname,
    upload_build_css_to,
    upload_source_css_to,
    upload_media_to,
    upload_media_thumbnail_to,
)


class Theme(MPTTModel):
    parent = TreeForeignKey(
        "self", on_delete=models.PROTECT, null=True, blank=True, related_name="children"
    )
    name = models.CharField(max_length=255)
    dirname = models.CharField(max_length=8, default=generate_theme_dirname)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    version = models.CharField(max_length=255, null=True, blank=True)
    author = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(max_length=255, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ["-is_default", "name"]

    def delete(self, *args, **kwargs):
        for css in self.css.all():
            css.delete()
        for media in self.media.all():
            media.delete()

        super().delete(*args, **kwargs)

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
    source_file = models.FileField(
        upload_to=upload_source_css_to, max_length=255, null=True, blank=True
    )
    source_hash = models.CharField(max_length=8, null=True, blank=True)
    source_needs_building = models.BooleanField(default=False)
    build_file = models.FileField(
        upload_to=upload_build_css_to, max_length=255, null=True, blank=True
    )
    build_hash = models.CharField(max_length=8, null=True, blank=True)
    size = models.PositiveIntegerField(default=0)

    order = models.IntegerField(default=0)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]

    def delete(self, *args, **kwargs):
        if self.source_file:
            self.source_file.delete(save=False)
        if self.build_file:
            self.build_file.delete(save=False)

        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name


class Media(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.PROTECT, related_name="media")

    name = models.CharField(max_length=255)
    file = models.ImageField(upload_to=upload_media_to, max_length=255)
    hash = models.CharField(max_length=8)
    type = models.CharField(max_length=255)
    width = models.PositiveIntegerField(default=0)
    height = models.PositiveIntegerField(default=0)
    size = models.PositiveIntegerField()
    thumbnail = models.ImageField(
        upload_to=upload_media_thumbnail_to, max_length=255, null=True, blank=True
    )
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def delete(self, *args, **kwargs):
        self.file.delete(save=False)
        if self.thumbnail:
            self.thumbnail.delete(save=False)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name
