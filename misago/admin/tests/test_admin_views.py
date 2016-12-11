from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..testutils import AdminTestCase
from ..views import get_protected_namespace


class FakeRequest(object):
    def __init__(self, path):
        self.path = path
        self.path_info = path


class AdminProtectedNamespaceTests(TestCase):
    def test_valid_cases(self):
        """get_protected_namespace returns true for protected links"""
        links_prefix = reverse('misago:admin:index')
        TEST_CASES = (
            '',
            'somewhere/',
            'ejksajdlksajldjskajdlksajlkdas',
        )

        for case in TEST_CASES:
            request = FakeRequest(links_prefix + case)
            self.assertEqual(get_protected_namespace(request), 'misago:admin')

    def test_invalid_cases(self):
        """get_protected_namespace returns none for other links"""
        TEST_CASES = (
            '/',
            '/somewhere/',
            '/ejksajdlksajldjskajdlksajlkdas',
        )

        for case in TEST_CASES:
            request = FakeRequest(case)
            self.assertEqual(get_protected_namespace(request), None)


class AdminLoginViewTests(TestCase):
    def test_login_returns_200_on_get(self):
        """unauthenticated request to admin index produces login form"""
        response = self.client.get(reverse('misago:admin:index'))

        self.assertContains(response, 'Sign in')
        self.assertContains(response, 'Username or e-mail')
        self.assertContains(response, 'Password')

    def test_login_returns_200_on_invalid_post(self):
        """form handles invalid data gracefully"""
        response = self.client.post(
            reverse('misago:admin:index'),
            data={'username': 'Nope', 'password': 'Nope'})

        self.assertContains(response, 'Login or password is incorrect.')
        self.assertContains(response, 'Sign in')
        self.assertContains(response, 'Username or e-mail')
        self.assertContains(response, 'Password')

    def test_login_returns_200_on_valid_post(self):
        """form handles valid data correctly"""
        User = get_user_model()
        User.objects.create_superuser('Bob', 'bob@test.com', 'Pass.123')

        response = self.client.post(
            reverse('misago:admin:index'),
            data={'username': 'Bob', 'password': 'Pass.123'})

        self.assertEqual(response.status_code, 302)


class AdminLogoutTests(AdminTestCase):
    def test_admin_logout(self):
        """admin logout logged from admin only"""
        response = self.client.post(reverse('misago:admin:logout'))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('misago:admin:index'))
        self.assertContains(response, "Your admin session has been closed.")

        response = self.client.get(reverse('misago:index'))
        self.assertContains(response, self.user.username)

    def test_complete_logout(self):
        """complete logout logged from both admin and site"""
        response = self.client.post(reverse('misago:logout'))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('misago:admin:index'))
        self.assertContains(response, "Sign in")

        response = self.client.get(reverse('misago:index'))
        self.assertContains(response, "Sign in")


class AdminIndexViewTests(AdminTestCase):
    def test_view_returns_200(self):
        """admin index view returns 200"""
        response = self.client.get(reverse('misago:admin:index'))

        self.assertContains(response, self.user.username)
