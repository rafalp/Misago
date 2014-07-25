from path import path
from PIL import Image

from django.contrib.auth import get_user_model
from django.test import TestCase

from misago.conf import settings

from misago.users.avatars import store, dynamic, gallery, gravatar
from misago.users.avatars.paths import AVATARS_STORE


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
            avatar = path('%s/%s_%s.png' % (avatar_dir, test_user.pk, size))
            self.assertTrue(avatar.exists())
            self.assertTrue(avatar.isfile())

        # Delete avatar and assert its gone
        store.delete_avatar(test_user)
        for size in settings.MISAGO_AVATARS_SIZES:
            avatar = path('%s/%s_%s.png' % (avatar_dir, test_user.pk, size))
            self.assertFalse(avatar.exists())

        # Override new avatar and test that it was changed
        store.store_avatar(test_user, test_image)
        store.store_new_avatar(test_user, test_image)
        for size in settings.MISAGO_AVATARS_SIZES:
            avatar = path('%s/%s_%s.png' % (avatar_dir, test_user.pk, size))
            self.assertTrue(avatar.exists())
            self.assertTrue(avatar.isfile())

        # Delete avatar
        store.delete_avatar(test_user)


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
            avatar = path('%s/%s_%s.png' % (avatar_dir, self.user.pk, size))
            self.assertFalse(avatar.exists())

    def assertAvatarWasSet(self):
        avatar_dir = store.get_existing_avatars_dir(self.user)
        for size in settings.MISAGO_AVATARS_SIZES:
            avatar = path('%s/%s_%s.png' % (avatar_dir, self.user.pk, size))
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
