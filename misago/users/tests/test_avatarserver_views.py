from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase

from misago.users.views.avatarserver import clean_size


class AvatarServerTests(TestCase):
    def test_user_avatar_serving(self):
        """avatar server handles user avatar requests"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@bob.com', 'pass123',
                                             set_default_avatar=True)

        avatar_url = reverse('misago:user-avatar', kwargs={
            'pk': test_user.pk,
            'hash': test_user.avatar_hash,
            'size': 150,
        })
        response = self.client.get(avatar_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/png')

    def test_deleted_user_avatar_serving(self):
        """avatar server handles deleted user avatar requests"""
        avatar_url = reverse('misago:user-avatar', kwargs={
            'pk': 12345,
            'hash': '12356af',
            'size': 150,
        })
        response = self.client.get(avatar_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/png')

    def test_blank_avatar_serving(self):
        """avatar server handles blank avatar requests"""
        response = self.client.get(reverse('misago:blank-avatar', kwargs={
            'size': 150,
        }))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/png')


class CleanSizeTests(TestCase):
    def test_size_too_big(self):
        """clean_size returns max for too big size"""
        max_size = max(settings.MISAGO_AVATARS_SIZES)
        too_big = max_size * 2

        self.assertEqual(clean_size(too_big), max_size)

    def test_size_too_small(self):
        """clean_size returns min for too small size"""
        min_size = min(settings.MISAGO_AVATARS_SIZES)
        too_small = min_size / 2

        self.assertEqual(clean_size(too_small), min_size)

    def test_mid_sizes(self):
        """clean_size returns approximates for little invalid sizes"""
        for size in settings.MISAGO_AVATARS_SIZES:
            self.assertEqual(clean_size(size - 1), size)

    def test_valid_sizes(self):
        """clean_size returns valid sizes untouched"""
        for size in settings.MISAGO_AVATARS_SIZES:
            self.assertEqual(clean_size(size), size)
