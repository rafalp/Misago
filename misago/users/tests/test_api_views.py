import json

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase


class ValidationAPITests(TestCase):
    ajax_header = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

    def test_validate_username(self):
        """test API for validating username"""
        response = self.client.get(reverse('misago:api_validate_username'))
        self.assertEqual(response.status_code, 405)

        response = self.client.post(reverse('misago:api_validate_username'),
                                    data={'username': 'Bob'},
                                    **self.ajax_header)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['has_error'], 0)
        self.assertIn('username', data['message'])

        User = get_user_model()
        user = User.objects.create_user("Bob", "bob@bob.com", "pass123")

        response = self.client.post(reverse('misago:api_validate_username'),
                                    data={'username': 'Bob'},
                                    **self.ajax_header)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['has_error'], 1)
        self.assertIn('not available', data['message'])

        test_url = reverse('misago:api_validate_username',
                           kwargs={'user_id': user.pk})

        response = self.client.post(
            test_url, data={'username': 'Bob'}, **self.ajax_header)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['has_error'], 0)
        self.assertIn('username', data['message'])

    def test_validate_email(self):
        """test API for validating email"""
        response = self.client.get(reverse('misago:api_validate_email'))
        self.assertEqual(response.status_code, 405)

        response = self.client.post(reverse('misago:api_validate_email'),
                                    data={'email': 'bob@bob.com'},
                                    **self.ajax_header)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['has_error'], 0)
        self.assertIn('e-mail', data['message'])

        User = get_user_model()
        user = User.objects.create_user("Bob", "bob@bob.com", "pass123")

        response = self.client.post(reverse('misago:api_validate_email'),
                                    data={'email': 'bob@bob.com'},
                                    **self.ajax_header)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['has_error'], 1)
        self.assertIn('not available', data['message'])

        test_url = reverse('misago:api_validate_email',
                           kwargs={'user_id': user.pk})

        response = self.client.post(
            test_url, data={'email': 'bob@bob.com'}, **self.ajax_header)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['has_error'], 0)
        self.assertIn('e-mail', data['message'])

    def test_validate_password(self):
        """test API for validating password"""
        response = self.client.get(reverse('misago:api_validate_password'))
        self.assertEqual(response.status_code, 405)

        response = self.client.post(reverse('misago:api_validate_password'),
                                    data={'password': 'pass123'},
                                    **self.ajax_header)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['has_error'], 0)
        self.assertIn('password', data['message'])

        response = self.client.post(reverse('misago:api_validate_password'),
                                    data={'password': 'p'},
                                    **self.ajax_header)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['has_error'], 1)
        self.assertIn('characters long', data['message'])
