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

    def __init__(self, user: Union["User", AnonymousUser], cache_versions: dict):
        self.user = user
        self.cache_versions = cache_versions
        self.accessed_permissions = False

    def __getattr__(self, name: str) -> Any:
        return self.permissions[name]

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

    @cached_property
    def categories_moderator(self) -> list[int]:
        if self.user.is_anonymous:
            return []

        if self.is_global_moderator:
            return self.permissions["categories"][CategoryPermission.BROWSE]

        if not self.permissions["categories"][CategoryPermission.BROWSE]:
            return []

        browsed_categories = set(
            self.permissions["categories"][CategoryPermission.BROWSE]
        )

        return list(browsed_categories.intersection(self.moderator.categories_ids))
