from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from misago.conf import settings


UserModel = get_user_model()


class AvatarServerTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user('Bob', 'bob@bob.com', 'Pass123')

        self.user.avatars = [
            {
                'size': 200,
                'url': '/media/avatars/avatar-200.png',
            },
            {
                'size': 100,
                'url': '/media/avatars/avatar-100.png',
            },
            {
                'size': 50,
                'url': '/media/avatars/avatar-50.png',
            },
        ]

        self.user.save()

    def test_get_user_avatar_exact_size(self):
        """avatar server resolved valid avatar url for user"""
        avatar_url = reverse(
            'misago:user-avatar',
            kwargs={
                'pk': self.user.pk,
                'size': 100,
            },
        )

        response = self.client.get(avatar_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], self.user.avatars[1]['url'])

    def test_get_user_avatar_inexact_size(self):
        """avatar server resolved valid avatar fallback for user"""
        avatar_url = reverse(
            'misago:user-avatar',
            kwargs={
                'pk': self.user.pk,
                'size': 150,
            },
        )

        response = self.client.get(avatar_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], self.user.avatars[0]['url'])

    def test_get_notfound_user_avatar(self):
        """avatar server handles deleted user avatar requests"""
        avatar_url = reverse(
            'misago:user-avatar',
            kwargs={
                'pk': self.user.pk + 1,
                'size': 150,
            },
        )
        response = self.client.get(avatar_url)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['location'].endswith(settings.MISAGO_BLANK_AVATAR))

    def test_blank_avatar_serving(self):
        """avatar server handles blank avatar requests"""
        response = self.client.get(reverse('misago:blank-avatar'))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['location'].endswith(settings.MISAGO_BLANK_AVATAR))
