from django.test import TestCase
from django.urls import reverse

from ...conf import settings
from ..test import create_test_user


class AvatarServerTests(TestCase):
    def setUp(self):
        self.user = create_test_user("User", "User@example.com")

    def test_get_user_avatar_exact_size(self):
        """avatar server resolved valid avatar url for user"""
        avatar_url = reverse(
            "misago:user-avatar", kwargs={"pk": self.user.pk, "size": 200}
        )

        response = self.client.get(avatar_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], self.user.avatars[1]["url"])

    def test_get_user_avatar_inexact_size(self):
        """avatar server resolved valid avatar fallback for user"""
        avatar_url = reverse(
            "misago:user-avatar", kwargs={"pk": self.user.pk, "size": 250}
        )

        response = self.client.get(avatar_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], self.user.avatars[0]["url"])

    def test_get_notfound_user_avatar(self):
        """avatar server handles deleted user avatar requests"""
        avatar_url = reverse(
            "misago:user-avatar", kwargs={"pk": self.user.pk + 1, "size": 150}
        )
        response = self.client.get(avatar_url)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response["location"].endswith(settings.MISAGO_BLANK_AVATAR))

    def test_blank_avatar_serving(self):
        """avatar server handles blank avatar requests"""
        response = self.client.get(reverse("misago:blank-avatar"))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response["location"].endswith(settings.MISAGO_BLANK_AVATAR))
