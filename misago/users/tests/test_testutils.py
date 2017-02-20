from django.urls import reverse

from misago.users.testutils import AuthenticatedUserTestCase, SuperUserTestCase, UserTestCase


class UserTestCaseTests(UserTestCase):
    def test_get_anonymous_user(self):
        """get_anonymous_user returns anon user instance"""
        user = self.get_anonymous_user()
        self.assertFalse(user.is_authenticated)
        self.assertTrue(user.is_anonymous)

    def test_get_authenticated_user(self):
        """get_authenticated_user returns auth user instance"""
        user = self.get_authenticated_user()
        self.assertTrue(user.is_authenticated)
        self.assertFalse(user.is_anonymous)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_get_superuser(self):
        """get_superuser returns auth user instance"""
        user = self.get_superuser()
        self.assertTrue(user.is_authenticated)
        self.assertFalse(user.is_anonymous)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_login_user(self):
        """login_user logs user"""
        user = self.get_authenticated_user()
        self.login_user(user)

        response = self.client.get('/api/auth/')
        self.assertEqual(response.status_code, 200)

        user_json = response.json()
        self.assertEqual(user_json['id'], user.id)

    def test_login_superuser(self):
        """login_user logs superuser"""
        user = self.get_superuser()
        self.login_user(user)

        response = self.client.get('/api/auth/')
        self.assertEqual(response.status_code, 200)

        user_json = response.json()
        self.assertEqual(user_json['id'], user.id)

    def test_logout_user(self):
        """logout_user logs user out"""
        user = self.get_authenticated_user()
        self.login_user(user)
        self.logout_user()

        response = self.client.get('/api/auth/')
        self.assertEqual(response.status_code, 200)

        user_json = response.json()
        self.assertIsNone(user_json['id'])

    def test_logout_superuser(self):
        """logout_user logs superuser out"""
        user = self.get_superuser()
        self.login_user(user)
        self.logout_user()

        response = self.client.get('/api/auth/')
        self.assertEqual(response.status_code, 200)

        user_json = response.json()
        self.assertIsNone(user_json['id'])


class AuthenticatedUserTestCaseTests(AuthenticatedUserTestCase):
    def test_setup(self):
        """setup executed correctly"""
        response = self.client.get(reverse('misago:index'))
        self.assertContains(response, self.user.username)

    def test_reload_user(self):
        """reload_user reloads user"""
        user_pk = self.user.pk

        self.reload_user()
        self.assertEqual(user_pk, self.user.pk)


class SuperUserTestCaseTests(SuperUserTestCase):
    def test_setup(self):
        """setup executed correctly"""
        self.assertTrue(self.user.is_staff)
        self.assertTrue(self.user.is_superuser)

        response = self.client.get('/api/auth/')
        self.assertEqual(response.status_code, 200)

        user_json = response.json()
        self.assertEqual(user_json['id'], self.user.id)
