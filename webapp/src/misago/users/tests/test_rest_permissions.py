from django.urls import reverse

from ..models import Ban
from ..test import UserTestCase, AuthenticatedUserTestCase


class UnbannedOnlyTests(AuthenticatedUserTestCase):
    # def setUp(self):
    #     self.user = self.get_authenticated_user()

    # no guests allowed anymore
    # def test_api_allows_guests(self):
    #     """policy allows guests"""
    #     response = self.client.post(
    #         reverse("misago:api:send-password-form"), data={"email": self.user.email}
    #     )
#     self.assertEqual(response.status_code, 200)

    def test_api_allows_authenticated(self):
        """policy allows authenticated"""
        response = self.client.post(
            reverse("misago:options"), data={"email": self.user.email}
        )
        self.assertEqual(response.status_code, 200)

    # ban signs out user, which results in redirect in middleware
    # def test_api_blocks_banned(self):
    #     """policy blocked banned ip"""
    #     Ban.objects.create(
    #         check_type=Ban.IP, banned_value="127.*", user_message="Ya got banned!"
    #     )

    #     response = self.client.post(
    #         reverse("misago:api:send-password-form"), data={"email": self.user.email}
    #     )
    #     self.assertEqual(response.status_code, 403)


class UnbannedAnonOnlyTests(AuthenticatedUserTestCase):

    # no guests allowed anymore
    # def test_api_allows_guests(self):
    #     """policy allows guests"""
    #     self.user.requires_activation = 1
    #     self.user.save()

    #     response = self.client.post(
    #         reverse("misago:api:send-activation"), data={"email": self.user.email}
    #     )
    #     self.assertEqual(response.status_code, 200)

    def test_api_allows_authenticated(self):
        """policy blocks authenticated"""
        response = self.client.post(
            reverse("misago:api:send-activation"), data={"email": self.user.email}
        )
        self.assertEqual(response.status_code, 403)

    # ban signs out user, which results in redirect in middleware
    # def test_api_blocks_banned(self):
    #     """policy blocked banned ip"""
    #     Ban.objects.create(
    #         check_type=Ban.IP, banned_value="127.*", user_message="Ya got banned!"
    #     )

    #     response = self.client.post(
    #         reverse("misago:api:send-activation"), data={"email": self.user.email}
    #     )
    #     self.assertEqual(response.status_code, 403)
