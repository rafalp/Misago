from django.test import override_settings
from django.urls import reverse

from misago.admin.testutils import AdminTestCase


@override_settings(ROOT_URLCONF='misago.core.testproject.urls')
class DjangoAdminAuthTests(AdminTestCase):
    """assertions for Django admin auth interop with Misago User Model"""

    def test_login(self):
        """its possible to sign in to django admin"""
        self.logout_user()

        # form renders
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)

        # form handles login
        response = self.client.post(
            reverse('admin:index'),
            data={
                'username': self.user.email,
                'password': self.USER_PASSWORD,
            },
        )
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    def test_logout(self):
        """its possible to sign out from django admin"""
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

        # assert there's no showstopper on signout page
        response = self.client.get(reverse('admin:logout'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.user.username)

        # user was signed out
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.user.username)
