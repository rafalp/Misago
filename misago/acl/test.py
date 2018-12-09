from functools import wraps
from unittest.mock import patch

from .useracl import get_user_acl

__all__ = ["patch_user_acl"]


class PatchUserACL:
    def patch_user_acl(self, user, patch):
        self.patches[user.id] = patch

    def patched_get_user_acl(self, user, cache_versions):
        user_acl = get_user_acl(user, cache_versions)
        user_acl.update(self.patches.get(user.id, {}))
        return user_acl

    def __enter__(self):
        self.patches = {}

    def __exit__(self, *_):
        self.patches = {}

    def __call__(self, f):
        @wraps(f)
        def inner(*args, **kwargs):
            with self as context:
                with patch(
                    "misago.acl.useracl.get_user_acl",
                    side_effect=self.patched_get_user_acl,
                ):
                    new_args = args + (self.patch_user_acl,)
                    return f(*new_args, **kwargs)
        
        return inner


patch_user_acl = PatchUserACL()