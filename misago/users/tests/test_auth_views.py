import json

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase


class AuthViewsTests(TestCase):
    def test_auth_views_return_302(self):
        """auth views should always return redirect"""
        response = self.client.get(reverse('misago:login'))
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('misago:login'))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('misago:logout'))
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('misago:logout'))
        self.assertEqual(response.status_code, 302)

    def test_login_view_redirect_to(self):
        """login view respects redirect_to POST"""
        # valid redirect
        response = self.client.post(reverse('misago:login'), data={
            'redirect_to': '/redirect/'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], 'http://testserver/redirect/')

        # invalid redirect (redirects to other site)
        response = self.client.post(reverse('misago:login'), data={
            'redirect_to': 'http://somewhereelse.com/page.html'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], 'http://testserver/')

        # in-dev ember-cli redirect
        conf_overrides = {
            'DEBUG': True,
            'MISAGO_EMBER_CLI_ORIGIN': 'http://localhost:4200'
        }

        with self.settings(**conf_overrides):
            # valid request, has Origin header
            response = self.client.post(reverse('misago:login'), data={
                'redirect_to': 'http://localhost:4200/page.html'
            }, HTTP_ORIGIN='http://localhost:4200')

            self.assertEqual(response.status_code, 302)
            self.assertEqual(response['location'],
                             'http://localhost:4200/page.html')

            # invalid request, different Origin header
            response = self.client.post(reverse('misago:login'), data={
                'redirect_to': 'http://localhost:4200/page.html'
            }, HTTP_ORIGIN='http://somewhere.com/')

            self.assertEqual(response.status_code, 302)
            self.assertEqual(response['location'], 'http://testserver/')

    def test_logout_view(self):
        """logout view logs user out on post"""
        response = self.client.post(
            '/api/auth/', data={'username': 'nope', 'password': 'nope'})

        self.assertEqual(response.status_code, 400)
        self.assertIn("Login or password is incorrect.", response.content)

        response = self.client.get('/api/auth/')
        self.assertEqual(response.status_code, 200)

        user_json = json.loads(response.content)
        self.assertIsNone(user_json['id'])

        response = self.client.post(reverse('misago:logout'))
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/api/auth/')
        self.assertEqual(response.status_code, 200)

        user_json = json.loads(response.content)
        self.assertIsNone(user_json['id'])
