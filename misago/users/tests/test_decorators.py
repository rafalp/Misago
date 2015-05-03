from django.core.urlresolvers import reverse
from misago.users.testutils import UserTestCase


class DenyAuthenticatedTests(UserTestCase):
    def test_success(self):
        """deny_authenticated decorator allowed guest request"""
        response = self.client.post('/api/auth/')
        self.assertEqual(response.status_code, 400)

    def test_fail(self):
        """deny_authenticated decorator denied authenticated request"""
        self.login_user(self.get_authenticated_user())

        response = self.client.post('/api/auth/')
        self.assertEqual(response.status_code, 403)


class DeflectAuthenticatedTests(UserTestCase):
    def test_success(self):
        """deflect_authenticated decorator allowed guest request"""
        response = self.client.get(reverse('misago:forgotten_password'))
        self.assertEqual(response.status_code, 200)

    def test_fail(self):
        """deflect_authenticated decorator deflected authenticated request"""
        self.login_user(self.get_authenticated_user())

        response = self.client.get(reverse('misago:forgotten_password'))
        self.assertEqual(response.status_code, 302)


class DeflectGuestsTests(UserTestCase):
    def test_success(self):
        """deflect_guests decorator allowed authenticated request"""
        self.login_user(self.get_authenticated_user())

        response = self.client.post(
            reverse('misago:usercp_change_forum_options'))
        self.assertEqual(response.status_code, 200)

    def test_fail(self):
        """deflect_guests decorator deflected authenticated request"""
        response = self.client.post(
            reverse('misago:usercp_change_forum_options'))
        self.assertEqual(response.status_code, 302)
