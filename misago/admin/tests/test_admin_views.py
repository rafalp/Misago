# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from misago.admin.testutils import AdminTestCase
from misago.admin.views import get_protected_namespace


UserModel = get_user_model()


class FakeRequest(object):
    def __init__(self, path):
        self.path = path
        self.path_info = path


class AdminProtectedNamespaceTests(TestCase):
    def test_valid_cases(self):
        """get_protected_namespace returns true for protected links"""
        links_prefix = reverse('misago:admin:index')
        TEST_CASES = ('', 'somewhere/', 'ejksajdlksajldjskajdlksajlkdas', )

        for case in TEST_CASES:
            request = FakeRequest(links_prefix + case)
            self.assertEqual(get_protected_namespace(request), 'misago:admin')

    def test_invalid_cases(self):
        """get_protected_namespace returns none for other links"""
        TEST_CASES = ('/', '/somewhere/', '/ejksajdlksajldjskajdlksajlkdas', )

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
            data={
                'username': 'Nope',
                'password': 'Nope',
            },
        )

        self.assertContains(response, "Login or password is incorrect.")
        self.assertContains(response, "Sign in")
        self.assertContains(response, "Username or e-mail")
        self.assertContains(response, "Password")

    def test_login_denies_non_staff_non_superuser(self):
        """login rejects user thats non staff and non superuser"""
        user = UserModel.objects.create_user('Bob', 'bob@test.com', 'Pass.123')

        user.is_staff = False
        user.is_superuser = False
        user.save()

        response = self.client.post(
            reverse('misago:admin:index'),
            data={
                'username': 'Bob',
                'password': 'Pass.123',
            },
        )

        self.assertContains(response, "Your account does not have admin privileges.")

    def test_login_denies_non_staff_superuser(self):
        """login rejects user thats non staff and superuser"""
        user = UserModel.objects.create_user('Bob', 'bob@test.com', 'Pass.123')

        user.is_staff = False
        user.is_superuser = True
        user.save()

        response = self.client.post(
            reverse('misago:admin:index'),
            data={
                'username': 'Bob',
                'password': 'Pass.123',
            },
        )

        self.assertContains(response, "Your account does not have admin privileges.")

    def test_login_signs_in_staff_non_superuser(self):
        """login passess user thats staff and non superuser"""
        user = UserModel.objects.create_user('Bob', 'bob@test.com', 'Pass.123')

        user.is_staff = True
        user.is_superuser = False
        user.save()

        response = self.client.post(
            reverse('misago:admin:index'),
            data={
                'username': 'Bob',
                'password': 'Pass.123',
            },
        )

        self.assertEqual(response.status_code, 302)

    def test_login_signs_in_staff_superuser(self):
        """login passess user thats staff and superuser"""
        user = UserModel.objects.create_user('Bob', 'bob@test.com', 'Pass.123')

        user.is_staff = True
        user.is_superuser = True
        user.save()

        response = self.client.post(
            reverse('misago:admin:index'),
            data={
                'username': 'Bob',
                'password': 'Pass.123',
            },
        )

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


class AdminViewAccessTests(AdminTestCase):
    def test_admin_denies_non_staff_non_superuser(self):
        """admin middleware rejects user thats non staff and non superuser"""
        self.user.is_staff = False
        self.user.is_superuser = False
        self.user.save()

        response = self.client.get(reverse('misago:admin:index'))
        self.assertContains(response, "Sign in")

    def test_admin_denies_non_staff_superuser(self):
        """admin middleware rejects user thats non staff and superuser"""
        self.user.is_staff = False
        self.user.is_superuser = True
        self.user.save()

        response = self.client.get(reverse('misago:admin:index'))
        self.assertContains(response, "Sign in")

    def test_admin_passess_in_staff_non_superuser(self):
        """admin middleware passess user thats staff and non superuser"""
        self.user.is_staff = True
        self.user.is_superuser = False
        self.user.save()

        response = self.client.get(reverse('misago:admin:index'))
        self.assertContains(response, self.user.username)

    def test_admin_passess_in_staff_superuser(self):
        """admin middleware passess user thats staff and superuser"""
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()

        response = self.client.get(reverse('misago:admin:index'))
        self.assertContains(response, self.user.username)


class AdminIndexViewTests(AdminTestCase):
    def test_view_returns_200(self):
        """admin index view returns 200"""
        response = self.client.get(reverse('misago:admin:index'))

        self.assertContains(response, self.user.username)


class Admin404ErrorTests(AdminTestCase):
    def test_list_search_unicode_handling(self):
        """querystring creation handles unicode strings"""
        test_link = '%stotally-errored/' % reverse('misago:admin:index')

        response = self.client.get(test_link)

        self.assertContains(response, "Requested page could not be found.", status_code=404)


class AdminGenericViewsTests(AdminTestCase):
    def test_view_redirected_queryvar(self):
        """querystring redirected value is handled"""
        test_link = reverse('misago:admin:users:accounts:index')

        # request resulted in redirect with redirected=1 bit
        response = self.client.get('%s?username=lorem' % test_link)
        self.assertEqual(response.status_code, 302)
        self.assertIn('redirected=1', response['location'])

        # request with flag muted redirect
        response = self.client.get('%s?redirected=1&username=lorem' % test_link)
        self.assertEqual(response.status_code, 200)

    def test_list_search_unicode_handling(self):
        """querystring creation handles unicode strings"""
        test_link = reverse('misago:admin:users:accounts:index')
        response = self.client.get('%s?redirected=1&username=%s' % (test_link, 'łut'))
        self.assertEqual(response.status_code, 200)
