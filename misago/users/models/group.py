from django.db import models
from django.utils.translation import pgettext

from ...plugins.models import PluginDataModel
from ..enums import CUSTOM_GROUP_ID_START, DefaultGroupId


class Group(PluginDataModel):
    name = models.CharField(max_length=150)
    slug = models.CharField(max_length=150, unique=True)

    user_title = models.CharField(max_length=150, null=True, blank=True)
    color = models.CharField(max_length=7, null=True, blank=True)
    icon = models.CharField(max_length=50, null=True, blank=True)
    css_suffix = models.CharField(max_length=50, null=True, blank=True)

    is_page = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)

    ordering = models.PositiveIntegerField(default=0)

    can_see_user_profiles = models.BooleanField(default=False)

    class Meta:
        indexes = PluginDataModel.Meta.indexes
        ordering = ["ordering"]

    def __str__(self) -> str:
        return pgettext("default user group", self.name)

    @property
    def is_admin(self):
        return self.id == DefaultGroupId.ADMINS

    @property
    def is_protected(self):
        return self.id < CUSTOM_GROUP_ID_START

    def translated_user_title(self) -> str | None:
        if self.user_title:
            return pgettext("default user group", self.user_title)
        return None


class GroupDescription(PluginDataModel):
    group = models.OneToOneField(
        Group,
        on_delete=models.PROTECT,
        primary_key=True,
        related_name="description",
    )
    markdown = models.TextField(null=True, blank=True)
    html = models.TextField(null=True, blank=True)
    meta = models.TextField(null=True, blank=True)
