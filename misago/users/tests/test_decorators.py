from django.core.urlresolvers import reverse
from misago.users.testutils import UserTestCase


class DenyAuthenticatedTests(UserTestCase):
    ajax_header = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

    def test_success(self):
        """deny_authenticated decorator allowed guest request"""
        response = self.client.get(reverse('misago:request_password_reset'))
        self.assertEqual(response.status_code, 200)

    def test_fail(self):
        """deny_authenticated decorator blocked authenticated request"""
        self.login_user(self.get_authenticated_user())

        response = self.client.get(reverse('misago:request_password_reset'))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('misago:request_password_reset'),
                                           **self.ajax_header)
        self.assertEqual(response.status_code, 403)


class DenyGuestsTests(UserTestCase):
    ajax_header = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

    def test_success(self):
        """deny_guests decorator allowed authenticated request"""
        self.login_user(self.get_authenticated_user())

        response = self.client.post(
            reverse('misago:usercp_change_forum_options'))
        self.assertEqual(response.status_code, 200)

    def test_fail(self):
        """deny_guests decorator blocked authenticated request"""
        response = self.client.post(
            reverse('misago:usercp_change_forum_options'))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(
            reverse('misago:usercp_change_forum_options'), **self.ajax_header)
        self.assertEqual(response.status_code, 403)
