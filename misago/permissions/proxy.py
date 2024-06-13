from functools import cached_property
from typing import TYPE_CHECKING, Any, Union

from django.contrib.auth.models import AnonymousUser

from ..users.enums import DefaultGroupId
from .enums import CategoryPermission
from .models import Moderator
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

    @cached_property
    def permissions(self) -> dict:
        return get_user_permissions(self.user, self.cache_versions)

    @property
    def is_global_moderator(self) -> bool:
        if self.user.is_anonymous:
            return False

        return bool(
            DefaultGroupId.ADMINS in self.user.groups_ids
            or DefaultGroupId.MODERATORS in self.user.groups_ids
        )

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
        moderated_categories = set(
            Moderator.objects.moderated_categories_ids(self.user)
        )

        return list(browsed_categories.intersection(moderated_categories))

    def __getattr__(self, name: str) -> Any:
        return self.permissions[name]
