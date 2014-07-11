from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase


class LoginViewTests(TestCase):
    def test_view_get_returns_200(self):
        """login view returns 200 on GET"""
        response = self.client.get(reverse('misago:login'))
        self.assertEqual(response.status_code, 200)

    def test_view_invalid_credentials(self):
        """login view returns 200 on invalid POST"""
        response = self.client.post(
            reverse('misago:login'),
            data={'username': 'nope', 'password': 'nope'})

        self.assertEqual(response.status_code, 200)
        self.assertIn("Your login or password is incorrect.", response.content)

    def test_view_signin(self):
        """login view signs user in"""
        User = get_user_model()
        User.objects.create_user('Bob', 'bob@test.com', 'Pass.123')

        response = self.client.post(
            reverse('misago:login'),
            data={'username': 'Bob', 'password': 'Pass.123'})

        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('misago:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Bob', response.content)
