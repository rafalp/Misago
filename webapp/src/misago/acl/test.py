from contextlib import ContextDecorator, ExitStack, contextmanager
from unittest.mock import patch

from .useracl import get_user_acl

__all__ = ["patch_user_acl"]


class patch_user_acl(ContextDecorator, ExitStack):
    """Testing utility that patches get_user_acl results

    Can be used as decorator or context manager.

    Patch should be a dict or callable.
    """

    _acl_patches = []

    def __init__(self, acl_patch):
        super().__init__()
        self.acl_patch = acl_patch

    def patched_get_user_acl(self, user, cache_versions):
        user_acl = get_user_acl(user, cache_versions)
        self.apply_acl_patches(user, user_acl)
        return user_acl

    def apply_acl_patches(self, user, user_acl):
        for acl_patch in self._acl_patches:
            self.apply_acl_patch(user, user_acl, acl_patch)

    def apply_acl_patch(self, user, user_acl, acl_patch):
        if callable(acl_patch):
            acl_patch(user, user_acl)
        else:
            user_acl.update(acl_patch)

    def __enter__(self):
        super().__enter__()
        self.enter_context(self.enable_acl_patch())
        self.enter_context(self.patch_user_acl())

    @contextmanager
    def enable_acl_patch(self):
        try:
            self._acl_patches.append(self.acl_patch)
            yield
        finally:
            self._acl_patches.pop(-1)

    def patch_user_acl(self):
        return patch(
            "misago.acl.useracl.get_user_acl", side_effect=self.patched_get_user_acl
        )
