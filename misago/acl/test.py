from functools import wraps
from unittest.mock import patch

from .useracl import get_user_acl

__all__ = ["patch_user_acl"]


class patch_user_acl:
    """Testing utility that patches get_user_acl results

    Patch should be a dict or callable.
    Can be used as decorator or context manager.
    """
    _global_patch = None
    _user_patches = {}

    def __init__(self, global_patch=None):
        self._global_patch = global_patch

    def patch_user_acl(self, user, patch):
        self._user_patches[user.id] = patch

    def patched_get_user_acl(self, user, cache_versions):
        user_acl = get_user_acl(user, cache_versions)
        self.apply_acl_patches(user, user_acl)
        return user_acl

    def apply_acl_patches(self, user, user_acl):
        if self._global_patch:
            self.apply_acl_patch(user, user_acl, self._global_patch)
        if user.id in self._user_patches:
            user_acl_patch = self._user_patches[user.id]
            self.apply_acl_patch(user, user_acl, user_acl_patch)

    def apply_acl_patch(self, user, user_acl, acl_patch):
        if callable(acl_patch):
            acl_patch(user, user_acl)
        else:
            user_acl.update(acl_patch)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self._user_patches = {}

    def __call__(self, f):
        @wraps(f)
        def inner(*args, **kwargs):
            with self:
                with patch(
                    "misago.acl.useracl.get_user_acl",
                    side_effect=self.patched_get_user_acl,
                ):
                    new_args = args + (self.patch_user_acl,)
                    return f(*new_args, **kwargs)
        
        return inner
