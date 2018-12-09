from django.contrib.auth import get_user_model
from django.test import TestCase

from misago.acl import useracl
from misago.acl.test import patch_user_acl

User = get_user_model()

cache_versions = {"acl": "abcdefgh"}


def callable_acl_patch(user, user_acl):
    user_acl["patched_for_user_id"] = user.id


class PatchingUserACLTests(TestCase):
    @patch_user_acl({"is_patched": True})
    def test_decorator_patches_all_users_acls_in_test(self):
        user = User.objects.create_user("User", "user@example.com")
        user_acl = useracl.get_user_acl(user, cache_versions)
        assert user_acl["is_patched"]

    def test_decorator_removes_patches_after_test(self):
        user = User.objects.create_user("User", "user@example.com")

        @patch_user_acl({"is_patched": True})
        def test_function(patch_user_acl):
            user_acl = useracl.get_user_acl(user, cache_versions)
            assert user_acl["is_patched"]

        user_acl = useracl.get_user_acl(user, cache_versions)
        assert "is_patched" not in user_acl

    def test_context_manager_patches_all_users_acls_in_test(self):
        user = User.objects.create_user("User", "user@example.com")
        with patch_user_acl({"can_rename_users": "patched"}):
            user_acl = useracl.get_user_acl(user, cache_versions)
            assert user_acl["can_rename_users"] == "patched"

    def test_context_manager_removes_patches_after_exit(self):
        user = User.objects.create_user("User", "user@example.com")

        with patch_user_acl({"is_patched": True}):
            user_acl = useracl.get_user_acl(user, cache_versions)
            assert user_acl["is_patched"]

        user_acl = useracl.get_user_acl(user, cache_versions)
        assert "is_patched" not in user_acl

    def test_context_manager_patches_specified_user_acl(self):
        user = User.objects.create_user("User", "user@example.com")
        with patch_user_acl(user, {"can_rename_users": "patched"}):
            user_acl = useracl.get_user_acl(user, cache_versions)
            assert user_acl["can_rename_users"] == "patched"

    def test_other_user_acl_is_not_changed_by_user_specific_context_manager(self):
        patched_user = User.objects.create_user("User", "user@example.com")
        other_user = User.objects.create_user("User2", "user2@example.com")
        with patch_user_acl(patched_user, {"can_rename_users": "patched"}):
            other_user_acl = useracl.get_user_acl(other_user, cache_versions)
            assert other_user_acl["can_rename_users"] != "patched"

    @patch_user_acl(callable_acl_patch)
    def test_callable_patch_is_called_with_user_and_acl_by_decorator(self):
        user = User.objects.create_user("User", "user@example.com")
        user_acl = useracl.get_user_acl(user, cache_versions)
        assert user_acl["patched_for_user_id"] == user.id

    def test_callable_patch_is_called_with_user_and_acl_by_context_manager(self):
        user = User.objects.create_user("User", "user@example.com")
        with patch_user_acl(callable_acl_patch):
            user_acl = useracl.get_user_acl(user, cache_versions)
            assert user_acl["patched_for_user_id"] == user.id
