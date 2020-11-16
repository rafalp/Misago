from pathlib import Path
from unittest.mock import Mock

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.crypto import get_random_string
from PIL import Image

from ...conf import settings
from ..avatars import dynamic, gallery, gravatar, set_default_avatar, store, uploaded
from ..models import Avatar, AvatarGallery
from ..test import create_test_user


class AvatarsStoreTests(TestCase):
    def test_store(self):
        """store successfully stores and deletes avatar"""
        user = create_test_user("User", "user@example.com")

        test_image = Image.new("RGBA", (100, 100), 0)
        store.store_new_avatar(user, test_image)

        # reload user
        user.refresh_from_db()

        # assert that avatars were stored in media
        avatars_dict = {}
        for avatar in user.avatar_set.all():
            self.assertTrue(avatar.image.url)
            self.assertEqual(avatar.url, avatar.image.url)

            avatars_dict[avatar.size] = avatar

        # asserts that user.avatars cache was set
        self.assertEqual(len(avatars_dict), len(settings.MISAGO_AVATARS_SIZES))
        self.assertEqual(len(user.avatars), len(settings.MISAGO_AVATARS_SIZES))
        self.assertEqual(len(user.avatars), len(avatars_dict))

        for avatar in user.avatars:
            self.assertIn(avatar["size"], settings.MISAGO_AVATARS_SIZES)
            self.assertEqual(avatar["url"], avatars_dict[avatar["size"]].url)

        # another avatar change deleted old avatars
        store.store_new_avatar(user, test_image)
        for old_avatar in avatars_dict.values():
            avatar_path = Path(old_avatar.image.path)
            self.assertFalse(avatar_path.exists())
            self.assertFalse(avatar_path.is_file())

            with self.assertRaises(Avatar.DoesNotExist):
                Avatar.objects.get(pk=old_avatar.pk)

        # and updated user avatars again
        new_avatars_dict = {}
        for size in settings.MISAGO_AVATARS_SIZES:
            avatar = user.avatar_set.get(size=size)

            self.assertTrue(avatar.image.url)
            self.assertEqual(avatar.url, avatar.image.url)

            new_avatars_dict[size] = avatar

        self.assertTrue(avatars_dict != new_avatars_dict)

        # asserts that user.avatars cache was updated
        self.assertEqual(len(user.avatars), len(settings.MISAGO_AVATARS_SIZES))
        for avatar in user.avatars:
            self.assertIn(avatar["size"], settings.MISAGO_AVATARS_SIZES)
            self.assertEqual(avatar["url"], new_avatars_dict[avatar["size"]].url)

        # delete avatar
        store.delete_avatar(user)

        for removed_avatar in new_avatars_dict.values():
            avatar_path = Path(removed_avatar.image.path)
            self.assertFalse(avatar_path.exists())
            self.assertFalse(avatar_path.is_file())

            with self.assertRaises(Avatar.DoesNotExist):
                Avatar.objects.get(pk=removed_avatar.pk)


class AvatarSetterTests(TestCase):
    def setUp(self):
        self.user = create_test_user("User", "user@example.com", avatars=None)

    def tearDown(self):
        store.delete_avatar(self.user)

    def get_current_user(self):
        self.user.refresh_from_db()
        return self.user

    def assertNoAvatarIsSet(self):
        user = self.get_current_user()
        self.assertFalse(user.avatars)

    def assertAvatarWasSet(self):
        user = self.get_current_user()

        avatars_dict = {}
        for avatar in user.avatar_set.all():
            avatar_path = Path(avatar.image.path)
            self.assertTrue(avatar_path.exists())
            self.assertTrue(avatar_path.is_file())

            avatars_dict[avatar.size] = avatar

        self.assertEqual(len(user.avatars), len(avatars_dict))
        self.assertEqual(len(user.avatars), len(settings.MISAGO_AVATARS_SIZES))

    def test_dynamic_avatar(self):
        """dynamic avatar gets created"""
        self.assertNoAvatarIsSet()
        dynamic.set_avatar(self.user)
        self.assertAvatarWasSet()

    def test_random_gallery_avatar_no_gallery(self):
        """runtime error is raised when no gallery exists"""
        with self.assertRaises(RuntimeError):
            gallery.set_random_avatar(self.user)

    def test_random_gallery_avatar(self):
        """dynamic avatar gets created"""
        gallery.load_avatar_galleries()

        self.assertNoAvatarIsSet()
        gallery.set_random_avatar(self.user)
        self.assertAvatarWasSet()

    def test_selected_gallery_avatar(self):
        """dynamic avatar gets created"""
        gallery.load_avatar_galleries()

        self.assertNoAvatarIsSet()
        test_avatar = AvatarGallery.objects.order_by("id").last()
        gallery.set_avatar(self.user, test_avatar)
        self.assertAvatarWasSet()

    def test_gravatar(self):
        """dynamic avatar gets created"""
        self.assertNoAvatarIsSet()
        self.user.set_email("rafio.xudb@gmail.com")
        gravatar.set_avatar(self.user)
        self.assertAvatarWasSet()

    def test_default_avatar_gravatar(self):
        """default gravatar gets set"""
        self.assertNoAvatarIsSet()
        set_default_avatar(self.user, "gravatar", "dynamic")
        self.assertAvatarWasSet()

    def test_default_avatar_gravatar_fallback_dynamic(self):
        """default gravatar fails but fallback dynamic works"""
        gibberish_email = "%s@%s.%s" % (
            get_random_string(6),
            get_random_string(6),
            get_random_string(3),
        )

        self.user.set_email(gibberish_email)
        self.user.save()

        self.assertNoAvatarIsSet()
        set_default_avatar(self.user, "gravatar", "dynamic")
        self.assertAvatarWasSet()

    def test_default_avatar_gravatar_fallback_empty_gallery(self):
        """default both gravatar and fallback fail set"""
        gibberish_email = "%s@%s.%s" % (
            get_random_string(6),
            get_random_string(6),
            get_random_string(3),
        )
        self.user.set_email(gibberish_email)
        self.user.save()

        self.assertNoAvatarIsSet()
        self.user.save()
        set_default_avatar(self.user, "gravatar", "gallery")
        self.assertAvatarWasSet()


class MockAvatarFile:
    def __init__(self, size=None, name=None, mime=None):
        self.size = size
        self.name = name
        self.content_type = mime


class UploadedAvatarTests(TestCase):
    def test_clean_crop(self):
        """crop validation and cleaning"""
        image = Image.new("RGBA", (200, 200), 0)
        with self.assertRaises(ValidationError):
            uploaded.clean_crop(image, "abc")
        with self.assertRaises(ValidationError):
            uploaded.clean_crop(image, {})
        with self.assertRaises(ValidationError):
            uploaded.clean_crop(image, {"offset": {"x": "ugabuga"}})

        with self.assertRaises(ValidationError):
            uploaded.clean_crop(image, {"offset": {"x": 0, "y": 0}, "zoom": -2})

        with self.assertRaises(ValidationError):
            uploaded.clean_crop(image, {"offset": {"x": 0, "y": 0}, "zoom": 2})

    def test_uploaded_image_size_validation(self):
        """uploaded image size is validated"""
        settings = Mock(avatar_upload_limit=1)  # no. of MBs

        image = MockAvatarFile(size=1025)
        with self.assertRaises(ValidationError):
            uploaded.validate_file_size(settings, image)

        image = MockAvatarFile(size=1024)
        uploaded.validate_file_size(settings, image)

    def test_uploaded_image_extension_validation(self):
        """uploaded image extension is validated"""
        for invalid_extension in (".txt", ".zip", ".py", ".tiff"):
            with self.assertRaises(ValidationError):
                image = MockAvatarFile(name="test%s" % invalid_extension)
                uploaded.validate_extension(image)

        for valid_extension in uploaded.ALLOWED_EXTENSIONS:
            image = MockAvatarFile(name="test%s" % valid_extension)
            uploaded.validate_extension(image)

    def test_uploaded_image_mime_validation(self):
        """uploaded image mime type is validated"""
        image = MockAvatarFile(mime="fake/mime")
        with self.assertRaises(ValidationError):
            uploaded.validate_mime(image)

        for valid_mime in uploaded.ALLOWED_MIME_TYPES:
            image = MockAvatarFile(mime=valid_mime)
            uploaded.validate_mime(image)
