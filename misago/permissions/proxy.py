from functools import cached_property
from typing import TYPE_CHECKING, Any, Union

from django.contrib.auth.models import AnonymousUser

from ..users.enums import DefaultGroupId
from .enums import CategoryPermission
from .models import Moderator
from .moderator import ModeratorPermissions
from .user import get_user_permissions

if TYPE_CHECKING:
    from ..users.models import User


class UserPermissionsProxy:
    user: Union["User", AnonymousUser]
    cache_versions: dict
    accessed_permissions: bool

    _wrapped = False

    # Type hints for permissions checks
    categories: dict[str, list[int]]
    can_use_private_threads: bool
    can_start_private_threads: bool
    private_thread_members_limit: int
    can_edit_own_threads: bool
    own_threads_edit_time_limit: int
    can_edit_own_posts: bool
    own_posts_edit_time_limit: int
    can_see_others_post_edits: int
    can_hide_own_post_edits: int
    own_post_edits_hide_time_limit: int
    own_delete_post_edits_time_limit: int
    exempt_from_flood_control: bool
    can_upload_attachments: int
    attachment_size_limit: int
    can_always_delete_own_attachments: bool
    can_start_polls: bool
    can_edit_own_polls: bool
    own_polls_edit_time_limit: int
    can_close_own_polls: bool
    own_polls_close_time_limit: int
    can_vote_in_polls: bool
    can_like_posts: bool
    can_see_own_post_likes: int
    can_see_others_post_likes: int
    can_change_username: bool
    username_changes_limit: int
    username_changes_expire: int
    username_changes_span: int
    can_see_user_profiles: bool

    def __init__(self, user: Union["User", AnonymousUser], cache_versions: dict):
        self.user = user
        self.cache_versions = cache_versions
        self.accessed_permissions = False

    def __getattr__(self, name: str) -> Any:
        try:
            return self.permissions[name]
        except KeyError as exc:
            valid_permissions = "', '".join(self.permissions)
            raise AttributeError(
                f"{exc} is not an 'UserPermissionsProxy' attribute or "
                f"one of valid permissions: '{valid_permissions}'"
            ) from exc

    @cached_property
    def permissions(self) -> dict:
        self.accessed_permissions = True
        return get_user_permissions(self.user, self.cache_versions)

    @cached_property
    def moderator(self) -> ModeratorPermissions | None:
        if self.user.is_anonymous:
            return None

        return Moderator.objects.get_moderator_permissions(self.user)

    @property
    def is_global_moderator(self) -> bool:
        if self.user.is_anonymous:
            return False

        if (
            DefaultGroupId.ADMINS in self.user.groups_ids
            or DefaultGroupId.MODERATORS in self.user.groups_ids
        ):
            return True

        return self.moderator.is_global

    @property
    def is_private_threads_moderator(self) -> bool:
        if self.user.is_anonymous:
            return False

        if self.is_global_moderator:
            return True

        return self.moderator.private_threads

    @cached_property
    def moderated_categories(self) -> set[int]:
        if self.user.is_anonymous:
            return set()

        if self.is_global_moderator:
            return set(self.permissions["categories"][CategoryPermission.BROWSE])

        if not self.permissions["categories"][CategoryPermission.BROWSE]:
            return set()

        browsed_categories = set(
            self.permissions["categories"][CategoryPermission.BROWSE]
        )

        return browsed_categories.intersection(self.moderator.categories_ids)

    def is_category_moderator(self, category_id: int) -> bool:
        if self.user.is_anonymous:
            return False

        if self.is_global_moderator:
            return True

        return category_id in self.moderated_categories

    @property
    def attachment_size_limit(self):
        return self.permissions["attachment_size_limit"] * 1024

    @property
    def attachment_storage_limit(self):
        return self.permissions["attachment_storage_limit"] * 1024 * 1024

    @property
    def unused_attachments_storage_limit(self):
        return self.permissions["unused_attachments_storage_limit"] * 1024 * 1024
