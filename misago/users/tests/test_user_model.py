from pathlib import Path

from django.test import TestCase

from ...conf import settings
from ...core.utils import slugify
from ..avatars import dynamic
from ..models import Avatar, User


class UserTests(TestCase):
    def test_anonymize_data(self):
        """anonymize_data sets username and slug to one defined in settings"""
        user = User.objects.create_user("User", "user@example.com")

        user.anonymize_data()
        self.assertEqual(user.username, settings.MISAGO_ANONYMOUS_USERNAME)
        self.assertEqual(user.slug, slugify(settings.MISAGO_ANONYMOUS_USERNAME))

    def test_user_avatar_files_are_deleted_together_with_user(self):
        """account deletion for user also deletes their avatar file"""
        user = User.objects.create_user("User", "user@example.com")
        dynamic.set_avatar(user)
        user.save()

        user_avatars = []
        for avatar in user.avatar_set.all():
            avatar_path = Path(avatar.image.path)
            self.assertTrue(avatar_path.exists())
            self.assertTrue(avatar_path.is_file())
            user_avatars.append(avatar)
        self.assertNotEqual(user_avatars, [])

        user.delete()

        for removed_avatar in user_avatars:
            avatar_path = Path(removed_avatar.image.path)
            self.assertFalse(avatar_path.exists())
            self.assertFalse(avatar_path.is_file())

            with self.assertRaises(Avatar.DoesNotExist):
                Avatar.objects.get(pk=removed_avatar.pk)

    def test_set_username(self):
        """set_username sets username and slug on model"""
        user = User()

        user.set_username("Username")
        self.assertEqual(user.username, "Username")
        self.assertEqual(user.slug, "username")

        self.assertEqual(user.get_username(), "Username")
        self.assertEqual(user.get_full_name(), "Username")
        self.assertEqual(user.get_short_name(), "Username")

    def test_set_email(self):
        """set_email sets email and hash on model"""
        user = User()

        user.set_email("us3R@EXample.com")
        self.assertEqual(user.email, "us3R@example.com")
        self.assertTrue(user.email_hash)

    def test_mark_for_delete(self):
        """mark_for_delete deactivates user and sets is_deleting_account flag"""
        user = User.objects.create_user("User", "user@example.com")
        user.mark_for_delete()
        self.assertFalse(user.is_active)
        self.assertTrue(user.is_deleting_account)

        user_from_db = User.objects.get(pk=user.pk)
        self.assertFalse(user_from_db.is_active)
        self.assertTrue(user_from_db.is_deleting_account)

    def test_get_real_name(self):
        """get_real_name returns user-set real name or none"""
        user = User.objects.create_user("User", "user@example.com")
        self.assertIsNone(user.get_real_name())

        user.profile_fields["real_name"] = "User Usererson"
        self.assertEqual(user.get_real_name(), "User Usererson")
