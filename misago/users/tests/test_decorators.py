from django.urls import reverse

from misago.core.utils import encode_json_html
from misago.users.models import Ban
from misago.users.testutils import UserTestCase


class DenyAuthenticatedTests(UserTestCase):
    def test_success(self):
        """deny_authenticated decorator allowed guest request"""
        response = self.client.post(reverse('misago:request-activation'))
        self.assertEqual(response.status_code, 200)

    def test_fail(self):
        """deny_authenticated decorator denied authenticated request"""
        self.login_user(self.get_authenticated_user())

        response = self.client.post(reverse('misago:request-activation'))
        self.assertEqual(response.status_code, 403)


class DenyGuestsTests(UserTestCase):
    def test_success(self):
        """deny_guests decorator allowed authenticated request"""
        self.login_user(self.get_authenticated_user())

        response = self.client.post(reverse('misago:options'))
        self.assertEqual(response.status_code, 200)

    def test_fail(self):
        """deny_guests decorator blocked guest request"""
        response = self.client.post(reverse('misago:options'))
        self.assertEqual(response.status_code, 403)


class DenyBannedIPTests(UserTestCase):
    def test_success(self):
        """deny_banned_ips decorator allowed unbanned request"""
        Ban.objects.create(
            check_type=Ban.IP,
            banned_value='83.*',
            user_message="Ya got banned!",
        )

        response = self.client.post(reverse('misago:request-activation'))
        self.assertEqual(response.status_code, 200)

    def test_fail(self):
        """deny_banned_ips decorator denied banned request"""
        Ban.objects.create(
            check_type=Ban.IP,
            banned_value='127.*',
            user_message="Ya got banned!",
        )

        response = self.client.post(reverse('misago:request-activation'))
        self.assertContains(response, encode_json_html("<p>Ya got banned!</p>"), status_code=403)
