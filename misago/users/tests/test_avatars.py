from path import Path
from PIL import Image

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from misago.conf import settings

from misago.users.avatars import store, dynamic, gallery, gravatar, uploaded


class AvatarsStoreTests(TestCase):
    def test_store(self):
        """store successfully stores and deletes avatar"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@bob.com', 'pass123')

        test_image = Image.new("RGBA", (100, 100), 0)
        store.store_avatar(test_user, test_image)

        # Assert that avatar was stored
        avatar_dir = store.get_existing_avatars_dir(test_user)
        for size in settings.MISAGO_AVATARS_SIZES:
            avatar = Path('%s/%s_%s.png' % (avatar_dir, test_user.pk, size))
            self.assertTrue(avatar.exists())
            self.assertTrue(avatar.isfile())

        # Delete avatar and assert its gone
        store.delete_avatar(test_user)
        for size in settings.MISAGO_AVATARS_SIZES:
            avatar = Path('%s/%s_%s.png' % (avatar_dir, test_user.pk, size))
            self.assertFalse(avatar.exists())

        # Override new avatar and test that it was changed
        store.store_avatar(test_user, test_image)
        store.store_new_avatar(test_user, test_image)
        for size in settings.MISAGO_AVATARS_SIZES:
            avatar = Path('%s/%s_%s.png' % (avatar_dir, test_user.pk, size))
            self.assertTrue(avatar.exists())
            self.assertTrue(avatar.isfile())

        # Compute avatar hash
        test_user.avatar_hash = store.get_avatar_hash(test_user)
        self.assertEqual(len(test_user.avatar_hash), 8)
        test_user.save(update_fields=['avatar_hash'])

        # Delete avatar
        store.delete_avatar(test_user)
        for size in settings.MISAGO_AVATARS_SIZES:
            avatar = Path('%s/%s_%s.png' % (avatar_dir, test_user.pk, size))
            self.assertFalse(avatar.exists())


class AvatarSetterTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            'Bob', 'kontakt@rpiton.com', 'pass123')
        store.delete_avatar(self.user)

    def tearDown(self):
        store.delete_avatar(self.user)

    def assertNoAvatarIsSet(self):
        avatar_dir = store.get_existing_avatars_dir(self.user)
        for size in settings.MISAGO_AVATARS_SIZES:
            avatar = Path('%s/%s_%s.png' % (avatar_dir, self.user.pk, size))
            self.assertFalse(avatar.exists())

    def assertAvatarWasSet(self):
        avatar_dir = store.get_existing_avatars_dir(self.user)
        for size in settings.MISAGO_AVATARS_SIZES:
            avatar = Path('%s/%s_%s.png' % (avatar_dir, self.user.pk, size))
            self.assertTrue(avatar.exists())
            self.assertTrue(avatar.isfile())

    def test_dynamic_avatar(self):
        """dynamic avatar gets created"""
        self.assertNoAvatarIsSet()
        dynamic.set_avatar(self.user)
        self.assertAvatarWasSet()

    def test_random_gallery_avatar(self):
        """dynamic avatar gets created"""
        self.assertNoAvatarIsSet()
        gallery.set_random_avatar(self.user)
        self.assertAvatarWasSet()

    def test_selected_gallery_avatar(self):
        """dynamic avatar gets created"""
        self.assertNoAvatarIsSet()
        gallery.set_avatar(self.user, 'avatars/Nature/serval.jpg')
        self.assertAvatarWasSet()

    def test_gravatar(self):
        """dynamic avatar gets created"""
        self.assertNoAvatarIsSet()
        gravatar.set_avatar(self.user)
        self.assertAvatarWasSet()


class MockAvatarFile(object):
    def __init__(self, size=None, name=None, mime=None):
        self.size = size
        self.name = name
        self.content_type = mime


class UploadedAvatarTests(TestCase):
    def test_crop(self):
        """crop validation and clear"""
        image = Image.new("RGBA", (200, 200), 0)
        with self.assertRaises(ValidationError):
            uploaded.crop_string_to_dict(image, "abc")
        with self.assertRaises(ValidationError):
            uploaded.crop_string_to_dict(image, "2,2,4,a")
        with self.assertRaises(ValidationError):
            uploaded.crop_string_to_dict(image, "300,300,400,400,0,0,10,10")

        uploaded.crop_string_to_dict(image, "200,200,90,90,0,0,90,90")

    def test_uploaded_image_size_validation(self):
        """uploaded image size is validated"""
        image = MockAvatarFile(size=settings.avatar_upload_limit * 2024)
        with self.assertRaises(ValidationError):
            uploaded.validate_file_size(image)

        image = MockAvatarFile(size=settings.avatar_upload_limit * 1000)
        uploaded.validate_file_size(image)

    def test_uploaded_image_extension_validation(self):
        """uploaded image extension is validated"""
        for invalid_extension in ('.txt', '.zip', '.py', '.tiff'):
            with self.assertRaises(ValidationError):
                image = MockAvatarFile(name='test%s' % invalid_extension)
                uploaded.validate_extension(image)

        for valid_extension in uploaded.ALLOWED_EXTENSIONS:
            image = MockAvatarFile(name='test%s' % valid_extension)
            uploaded.validate_extension(image)

    def test_uploaded_image_mime_validation(self):
        """uploaded image mime type is validated"""
        image = MockAvatarFile(mime='fake/mime')
        with self.assertRaises(ValidationError):
            uploaded.validate_mime(image)

        for valid_mime in uploaded.ALLOWED_MIME_TYPES:
            image = MockAvatarFile(mime=valid_mime)
            uploaded.validate_mime(image)
