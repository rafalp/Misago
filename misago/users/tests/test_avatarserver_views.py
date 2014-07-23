from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.template import Context, Template
from django.test import TestCase


class AvatarServerTests(TestCase):
    def test_user_avatar_serving(self):
        """avatar server handles user avatar requests"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@bob.com', 'pass123',
                                             set_default_avatar=True)

        avatar_url = reverse('misago:user_avatar',
                             kwargs={'user_id': test_user.pk, 'size': 150})
        response = self.client.get(avatar_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/png')

    def test_deleted_user_avatar_serving(self):
        """avatar server handles deleted user avatar requests"""
        avatar_url = reverse('misago:user_avatar',
                             kwargs={'user_id': 123, 'size': 150})
        response = self.client.get(avatar_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/png')

    def test_blank_avatar_serving(self):
        """avatar server handles blank avatar requests"""
        response = self.client.get(reverse('misago:blank_avatar',
                                           kwargs={'size': 150}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/png')
