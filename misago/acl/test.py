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

    def __init__(self, *args):
        super().__init__()

        self._global_patch = None
        self._user_patches = {}

        if len(args) == 2:
            user, patch = args
            self._user_patches[user.id] = patch
        elif len(args) == 1:
            self._global_patch = args[0]
        else:
            raise ValueError("patch_user_acl takes one or two arguments.")

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
