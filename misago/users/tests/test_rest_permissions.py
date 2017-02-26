from django.urls import reverse

from misago.users.models import Ban
from misago.users.testutils import UserTestCase


class UnbannedOnlyTests(UserTestCase):
    def setUp(self):
        self.user = self.get_authenticated_user()

    def test_api_allows_guests(self):
        """policy allows guests"""
        response = self.client.post(
            reverse('misago:api:send-password-form'),
            data={
                'email': self.user.email,
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_api_allows_authenticated(self):
        """policy allows authenticated"""
        self.login_user(self.user)

        response = self.client.post(
            reverse('misago:api:send-password-form'),
            data={
                'email': self.user.email,
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_api_blocks_banned(self):
        """policy blocked banned ip"""
        Ban.objects.create(
            check_type=Ban.IP,
            banned_value='127.*',
            user_message='Ya got banned!',
        )

        response = self.client.post(
            reverse('misago:api:send-password-form'),
            data={
                'email': self.user.email,
            },
        )
        self.assertEqual(response.status_code, 403)


class UnbannedAnonOnlyTests(UserTestCase):
    def setUp(self):
        self.user = self.get_authenticated_user()

    def test_api_allows_guests(self):
        """policy allows guests"""
        self.user.requires_activation = 1
        self.user.save()

        response = self.client.post(
            reverse('misago:api:send-activation'),
            data={
                'email': self.user.email,
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_api_allows_authenticated(self):
        """policy blocks authenticated"""
        self.login_user(self.user)

        response = self.client.post(
            reverse('misago:api:send-activation'),
            data={
                'email': self.user.email,
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_api_blocks_banned(self):
        """policy blocked banned ip"""
        Ban.objects.create(
            check_type=Ban.IP,
            banned_value='127.*',
            user_message='Ya got banned!',
        )

        response = self.client.post(
            reverse('misago:api:send-activation'),
            data={
                'email': self.user.email,
            },
        )
        self.assertEqual(response.status_code, 403)
