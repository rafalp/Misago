from django.db import models

from ...plugins.models import PluginDataModel


class Group(PluginDataModel):
    name = models.CharField(max_length=150)
    slug = models.CharField(max_length=150, unique=True)

    user_icon = models.CharField(max_length=50, null=True, blank=True)
    user_title = models.CharField(max_length=150, null=True, blank=True)
    css_suffix = models.CharField(max_length=50, null=True, blank=True)

    ordering = models.PositiveIntegerField(default=0)
    is_list_tab = models.BooleanField(default=False, unique=True)

    is_default = models.BooleanField(default=False, unique=True)

    is_admin = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)

    class Meta:
        ordering = ["ordering"]
