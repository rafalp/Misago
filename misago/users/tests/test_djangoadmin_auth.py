from django.core.urlresolvers import reverse

from misago.admin.testutils import AdminTestCase


class DjangoAdminAuthTests(AdminTestCase):
    """assertions for Django admin auth interop with Misago User Model"""
    urls = 'misago.core.testproject.urls'

    def test_login(self):
        """its possible to sign in to django admin"""
        self.logout_user()

        # form renders
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)

        # form handles login
        response = self.client.post(reverse('admin:index'), data={
            'username': self.user.email,
            'password': self.USER_PASSWORD,
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user.username, response.content)

    def test_logout(self):
        """its possible to sign out from django admin"""
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user.username, response.content)

        # assert there's no showstopper on signout page
        response = self.client.get(reverse('admin:logout'))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.user.username, response.content)

        # user was signed out
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.user.username, response.content)
