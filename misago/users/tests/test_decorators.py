from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase


class DenyAuthenticatedTests(TestCase):
    def test_success(self):
        """deny_authenticated decorator allowed guest request"""
        response = self.client.get(reverse('misago:login'))
        self.assertEqual(response.status_code, 200)

    def test_fail(self):
        """deny_authenticated decorator blocked authenticated request"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@test.com', 'Pass.123')
        self.client.login(username=test_user.username, password='Pass.123')

        response = self.client.get(reverse('misago:login'))
        self.assertEqual(response.status_code, 403)


class DenyGuestsTests(TestCase):
    def test_success(self):
        """deny_guests decorator allowed authenticated request"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@test.com', 'Pass.123')
        self.client.login(username=test_user.username, password='Pass.123')

        response = self.client.post(reverse('misago:logout'))
        self.assertEqual(response.status_code, 302)

    def test_fail(self):
        """deny_guests decorator blocked authenticated request"""
        response = self.client.post(reverse('misago:logout'))
        self.assertEqual(response.status_code, 403)
