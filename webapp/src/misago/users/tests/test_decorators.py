from django.urls import reverse

from ...core.utils import encode_json_html
from ..models import Ban
from ..test import UserTestCase

from misago.users.test import AuthenticatedUserTestCase


class DenyAuthenticatedTests(AuthenticatedUserTestCase):

    # there is no longer any unauthenticated state
    # def test_success(self):
    #     """deny_authenticated decorator allowed guest request"""
    #     response = self.client.post(reverse("misago:request-activation"))
    #     self.assertEqual(response.status_code, 200)

    def test_fail(self):
        """deny_authenticated decorator denied authenticated request"""
        response = self.client.post(reverse("misago:request-activation"))
        self.assertEqual(response.status_code, 403)


class DenyGuestsTests(AuthenticatedUserTestCase):
    def test_success(self):
        """deny_guests decorator allowed authenticated request"""
        response = self.client.post(reverse("misago:options"))
        self.assertEqual(response.status_code, 200)

    # there is no longer any unauthenticated state
    # def test_fail(self):
    #     """deny_guests decorator blocked guest request"""
    #     response = self.client.post(reverse("misago:options"))
    #     self.assertEqual(response.status_code, 403)

    # def test_ref_login(self):
    #     """deny_guests decorator redirected guest request to homepage if ref=login"""
    #     response = self.client.post("%s?ref=login" % reverse("misago:options"))
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response["location"], reverse("misago:index"))


class DenyBannedIPTests(AuthenticatedUserTestCase):
    def test_success(self):
        """deny_banned_ips decorator allowed unbanned request"""
        Ban.objects.create(
            check_type=Ban.IP, banned_value="83.*", user_message="Ya got banned!"
        )

        response = self.client.post(reverse("misago:options"))
        self.assertEqual(response.status_code, 200)

    # ban signs out user, which results in redirect in middleware
    # def test_fail(self):
    #     """deny_banned_ips decorator denied banned request"""
    #     Ban.objects.create(
    #         check_type=Ban.IP, banned_value="127.*", user_message="Ya got banned!"
    #     )

    #     response = self.client.post(reverse("misago:options"))
    #     self.assertContains(
    #         response, encode_json_html("<p>Ya got banned!</p>"), status_code=403
    #     )
