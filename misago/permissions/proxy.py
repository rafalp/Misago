from functools import cached_property
from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from .user import get_user_permissions

User = get_user_model()


class UserPermissionsProxy:
    user: User | AnonymousUser
    cache_versions: dict
    accessed_permissions: bool

    _wrapped = False

    def __init__(self, user: User | AnonymousUser, cache_versions: dict):
        self.user = user
        self.cache_versions = cache_versions
        self.accessed_permissions = False

    @cached_property
    def permissions(self):
        self.accessed_permissions = True
        return get_user_permissions(self.user, self.cache_versions)

    def __getattr__(self, name: str) -> Any:
        return self.permissions[name]
