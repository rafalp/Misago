from django.db import models
from django.utils.translation import pgettext

from ...plugins.models import PluginDataModel


class Group(PluginDataModel):
    name = models.CharField(max_length=150)
    slug = models.CharField(max_length=150, unique=True)

    user_icon = models.CharField(max_length=50, null=True, blank=True)
    user_title = models.CharField(max_length=150, null=True, blank=True)
    css_suffix = models.CharField(max_length=50, null=True, blank=True)

    ordering = models.PositiveIntegerField(default=0)
    is_list_tab = models.BooleanField(default=False)

    is_default = models.BooleanField(default=False)

    class Meta:
        indexes = PluginDataModel.Meta.indexes
        ordering = ["ordering"]

    def __str__(self) -> str:
        return pgettext("default user group", self.name)

    def translated_user_title(self) -> str | None:
        if self.user_title:
            return pgettext(pgettext("default user group", self.user_title))
        return None
