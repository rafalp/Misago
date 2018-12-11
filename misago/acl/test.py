from contextlib import ExitStack
from functools import wraps
from unittest.mock import patch

from .useracl import get_user_acl

__all__ = ["patch_user_acl"]


class patch_user_acl(ExitStack):
    """Testing utility that patches get_user_acl results

    Can be used as decorator or context manager.
    
    Accepts one or two arguments:
    - patch_user_acl(acl_patch)
    - patch_user_acl(user, acl_patch)

    Patch should be a dict or callable.
    """

    def __init__(self, *patches):
        super().__init__()
        self._patches = patches

    def patched_get_user_acl(self, user, cache_versions):
        user_acl = get_user_acl(user, cache_versions)
        self.apply_acl_patches(user, user_acl)
        return user_acl

    def apply_acl_patches(self, user, user_acl):
        for acl_patch in self._patches:
            self.apply_acl_patch(user, user_acl, acl_patch)

    def apply_acl_patch(self, user, user_acl, acl_patch):
        if callable(acl_patch):
            acl_patch(user, user_acl)
        else:
            user_acl.update(acl_patch)

    def __enter__(self):
        super().__enter__()
        self.enter_context(
            patch(
                "misago.acl.useracl.get_user_acl",
                side_effect=self.patched_get_user_acl,
            )
        )

    def __call__(self, f):
        @wraps(f)
        def inner(*args, **kwargs):
            with self:
                with patch(
                    "misago.acl.useracl.get_user_acl",
                    side_effect=self.patched_get_user_acl,
                ):
                    return f(*args, **kwargs)
        
        return inner
