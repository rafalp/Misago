from django.contrib.auth import get_user_model
from django.test import TestCase

from misago.acl import useracl
from misago.acl.test import patch_user_acl

User = get_user_model()

cache_versions = {"acl": "abcdefgh"}


class PatchingUserACLInTestsTests(TestCase):
    @patch_user_acl
    def test_decorator_adds_patching_function_to_test(self, patch_user_acl):
        assert patch_user_acl

    @patch_user_acl
    def test_patching_function_changes_user_permission_value(self, patch_user_acl):
        user = User.objects.create_user("User", "user@example.com")
        patch_user_acl(user, {"can_rename_users": 123})
        user_acl = useracl.get_user_acl(user, cache_versions)
        assert user_acl["can_rename_users"] == 123

    @patch_user_acl
    def test_patching_function_adds_user_permission(self, patch_user_acl):
        user = User.objects.create_user("User", "user@example.com")
        patch_user_acl(user, {"new_user_permission": 123})
        user_acl = useracl.get_user_acl(user, cache_versions)
        assert user_acl["new_user_permission"] == 123

    def test_acl_patches_are_removed_after_test(self):
        user = User.objects.create_user("User", "user@example.com")

        @patch_user_acl
        def test_function(patch_user_acl):
            patch_user_acl(user, {"is_patched": True})
            user_acl = useracl.get_user_acl(user, cache_versions)
            assert user_acl["is_patched"]

        user_acl = useracl.get_user_acl(user, cache_versions)
        assert "is_patched" not in user_acl
    