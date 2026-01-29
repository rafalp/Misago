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

    can_edit_own_threads = models.BooleanField(default=False)
    own_threads_edit_time_limit = models.PositiveIntegerField(default=0)
    can_edit_own_posts = models.BooleanField(default=False)
    own_posts_edit_time_limit = models.PositiveIntegerField(default=0)
    can_see_others_post_edits = models.PositiveIntegerField(default=0)
    can_hide_own_post_edits = models.PositiveIntegerField(default=0)
    own_post_edits_hide_time_limit = models.PositiveIntegerField(default=0)
    own_delete_post_edits_time_limit = models.PositiveIntegerField(default=0)
    exempt_from_flood_control = models.BooleanField(default=False)

    can_use_private_threads = models.BooleanField(default=False)
    can_start_private_threads = models.BooleanField(default=False)
    private_thread_members_limit = models.PositiveIntegerField(default=1)

    can_upload_attachments = models.PositiveIntegerField(default=0)
    attachment_storage_limit = models.PositiveIntegerField(default=512)
    unused_attachments_storage_limit = models.PositiveIntegerField(default=64)
    attachment_size_limit = models.PositiveIntegerField(default=1000)
    can_always_delete_own_attachments = models.BooleanField(default=False)

    can_start_polls = models.BooleanField(default=False)
    can_edit_own_polls = models.BooleanField(default=False)
    own_polls_edit_time_limit = models.PositiveIntegerField(default=0)
    can_close_own_polls = models.BooleanField(default=False)
    own_polls_close_time_limit = models.PositiveIntegerField(default=0)
    can_vote_in_polls = models.BooleanField(default=False)

    can_like_posts = models.BooleanField(default=False)
    can_see_own_post_likes = models.PositiveIntegerField(default=0)
    can_see_others_post_likes = models.PositiveIntegerField(default=0)

    can_change_username = models.BooleanField(default=False)
    username_changes_limit = models.PositiveIntegerField(default=0)
    username_changes_expire = models.PositiveIntegerField(default=0)
    username_changes_span = models.PositiveIntegerField(default=0)

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
