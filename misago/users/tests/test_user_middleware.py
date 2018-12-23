from django.urls import reverse

from ..bans import ban_ip, ban_user
from ..models import Ban
from ..test import AuthenticatedUserTestCase


class UserMiddlewareTest(AuthenticatedUserTestCase):
    def setUp(self):
        super().setUp()

        self.api_link = reverse("misago:api:auth")
        self.test_link = reverse("misago:index")

    def test_banned_user(self):
        """middleware handles user that has been banned in meantime"""
        ban_user(self.user)

        response = self.client.get(self.test_link)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json()["id"])

    def test_banned_staff(self):
        """middleware handles staff user that has been banned in meantime"""
        self.user.is_staff = True
        self.user.save()

        ban_user(self.user)

        response = self.client.get(self.test_link)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], self.user.pk)

    def test_registration_only_ban(self):
        """middleware ignores registration only bans"""
        Ban.objects.create(
            check_type=Ban.USERNAME,
            banned_value="%s*" % self.user.username[:3],
            registration_only=True,
        )

        response = self.client.get(self.test_link)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], self.user.pk)

    def test_ip_banned_user(self):
        """middleware handles user that has been banned in meantime"""
        ban_ip("127.0.0.1")

        response = self.client.get(self.test_link)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json()["id"])

    def test_ip_banned_staff(self):
        """middleware handles staff user that has been banned in meantime"""
        self.user.is_staff = True
        self.user.save()

        ban_ip("127.0.0.1")

        response = self.client.get(self.test_link)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.api_link)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], self.user.pk)
