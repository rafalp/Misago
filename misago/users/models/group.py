from django.db import models
from django.utils.translation import pgettext

from ...permissions.enums import (
    CanHideOwnPostEdits,
    CanSeePostEdits,
    CanSeePostLikes,
    CanUploadAttachments,
    PermissionValue,
)
from ...plugins.models import PluginDataModel
from ..enums import CUSTOM_GROUP_ID_START, DefaultGroupId


class GroupQueryset(models.QuerySet):
    def defer_descriptions(self):
        return self.defer("description", "description_parsed", "meta_description")


class Group(PluginDataModel):
    name = models.CharField(max_length=150)
    slug = models.CharField(max_length=150, unique=True)

    description = models.TextField(null=True, blank=True)
    description_parsed = models.TextField(null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)

    user_title = models.CharField(max_length=150, null=True, blank=True)
    color = models.CharField(max_length=7, null=True, blank=True)
    icon = models.CharField(max_length=50, null=True, blank=True)
    css_suffix = models.CharField(max_length=50, null=True, blank=True)

    is_page = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)

    ordering = models.PositiveIntegerField(default=0)

    can_search = models.PositiveIntegerField(default=PermissionValue.NO)

    can_edit_own_threads = models.PositiveIntegerField(default=PermissionValue.NO)
    own_threads_edit_time_limit = models.PositiveIntegerField(default=0)
    can_edit_own_posts = models.PositiveIntegerField(default=PermissionValue.NO)
    own_posts_edit_time_limit = models.PositiveIntegerField(default=0)
    can_see_others_post_edits = models.PositiveIntegerField(default=CanSeePostEdits.NO)
    can_hide_own_post_edits = models.PositiveIntegerField(
        default=CanHideOwnPostEdits.NO
    )
    own_post_edits_hide_time_limit = models.PositiveIntegerField(default=0)
    own_delete_post_edits_time_limit = models.PositiveIntegerField(default=0)
    bypass_flood_control = models.PositiveIntegerField(default=PermissionValue.NO)
    bypass_content_approval = models.PositiveIntegerField(default=PermissionValue.NO)

    can_use_private_threads = models.PositiveIntegerField(default=PermissionValue.NO)
    can_start_private_threads = models.PositiveIntegerField(default=PermissionValue.NO)
    private_thread_members_limit = models.PositiveIntegerField(default=1)

    can_upload_attachments = models.PositiveIntegerField(
        default=CanUploadAttachments.NO
    )
    attachment_storage_limit = models.PositiveIntegerField(default=512)
    unused_attachments_storage_limit = models.PositiveIntegerField(default=64)
    attachment_size_limit = models.PositiveIntegerField(default=1000)
    can_always_delete_own_attachments = models.PositiveIntegerField(
        default=PermissionValue.NO
    )

    can_start_polls = models.PositiveIntegerField(default=PermissionValue.NO)
    can_edit_own_polls = models.PositiveIntegerField(default=PermissionValue.NO)
    own_polls_edit_time_limit = models.PositiveIntegerField(default=0)
    can_close_own_polls = models.PositiveIntegerField(default=PermissionValue.NO)
    own_polls_close_time_limit = models.PositiveIntegerField(default=0)
    can_vote_in_polls = models.PositiveIntegerField(default=PermissionValue.NO)

    can_like_posts = models.PositiveIntegerField(default=PermissionValue.NO)
    can_see_own_post_likes = models.PositiveIntegerField(default=CanSeePostLikes.NO)
    can_see_others_post_likes = models.PositiveIntegerField(default=CanSeePostLikes.NO)

    can_select_own_thread_solutions = models.PositiveIntegerField(
        default=PermissionValue.NO
    )
    can_change_own_thread_solutions = models.PositiveIntegerField(
        default=PermissionValue.NO
    )
    own_thread_solutions_change_time_limit = models.PositiveIntegerField(default=0)
    can_clear_own_thread_solutions = models.PositiveIntegerField(
        default=PermissionValue.NO
    )
    own_thread_solutions_clear_time_limit = models.PositiveIntegerField(default=0)

    can_change_username = models.PositiveIntegerField(default=PermissionValue.NO)
    username_changes_limit = models.PositiveIntegerField(default=0)
    username_changes_expire = models.PositiveIntegerField(default=0)
    username_changes_span = models.PositiveIntegerField(default=0)

    can_see_user_profiles = models.PositiveIntegerField(default=PermissionValue.NO)

    objects = GroupQueryset.as_manager()

    class Meta(PluginDataModel.Meta):
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
