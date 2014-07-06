from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase

from misago.conf import settings


class RegisterDecoratorTests(TestCase):
    def test_register_decorator_calls_valid_view_200(self):
        """login view returns 200 on GET"""
        settings.override_setting('account_activation', 'disabled')

        response = self.client.get(reverse('misago:register'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('new registrations are not currently accepted',
                      response.content)

        settings.override_setting('account_activation', 'none')
        response = self.client.get(reverse('misago:register'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Register new account',
                      response.content)

        settings.reset_settings()


class RegisterViewTests(TestCase):
    def test_register_view_get_returns_200(self):
        """register view returns 200 on GET"""
        response = self.client.get(reverse('misago:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_view_post_returns_302(self):
        """register view creates user on POST"""
        response = self.client.post(reverse('misago:register'))
        self.assertEqual(response.status_code, 200)
