from django.contrib.auth import get_user_model
from django.test import TestCase


class LoginViewTests(TestCase):
    def test_view_get_returns_200(self):
        """login view returns 200 on GET"""
        response = self.client.get(reverse('misago:login'))
        self.assertEqual(response.status_code, 200)

    def test_view_post_returns_200(self):
        """login view returns 200 on POST"""
        response = self.client.post(
            reverse('misago:login')
            data={'username': 'nope', 'password': 'nope'})

        self.assertEqual(response.status_code, 200)
        self.assertIn(response.content, "Your login or password is incorrect.")

    def test_view_post_creds_returns_200(self):
        """login view returns 200 on POST with signin credentials"""

        User = get_user_model()
        User.objects.create_user('Bob', 'bob@test.com', 'Pass.123')

        response = self.client.post(
            reverse('misago:login')
            data={'username': 'Bob', 'password': 'Pass.123'})

        self.assertEqual(response.status_code, 301)
