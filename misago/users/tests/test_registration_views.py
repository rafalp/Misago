from django.contrib.auth import get_user_model
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

from misago.conf import settings


class RegisterDecoratorTests(TestCase):
    def tearDown(self):
        settings.reset_settings()

    def test_register_decorator_calls_valid_view_200(self):
        """register decorator calls valid view"""
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


class RegisterViewTests(TestCase):
    def test_register_view_get_returns_200(self):
        """register view returns 200 on GET"""
        response = self.client.get(reverse('misago:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_view_post_creates_active_user(self):
        """register view creates active and signed in user on POST"""
        settings.override_setting('account_activation', 'none')

        response = self.client.post(reverse('misago:register'),
                                    data={'username': 'Bob',
                                          'email': 'bob@bob.com',
                                          'password': 'pass123'})
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('misago:index'))
        self.assertIn('Bob', response.content)

        User = get_user_model()
        user = User.objects.get_by_username('Bob')
        user = User.objects.get_by_email('bob@bob.com')

        response = self.client.get(reverse('misago:index'))
        self.assertIn('Bob', response.content)

        self.assertIn('Welcome', mail.outbox[0].subject)

    def test_register_view_post_creates_inactive_user(self):
        """register view creates inactive user on POST"""
        settings.override_setting('account_activation', 'user')

        response = self.client.post(reverse('misago:register'),
                                    data={'username': 'Bob',
                                          'email': 'bob@bob.com',
                                          'password': 'pass123'})
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('misago:register_completed'))
        self.assertIn('bob@bob.com', response.content)

        User = get_user_model()
        user = User.objects.get_by_username('Bob')
        user = User.objects.get_by_email('bob@bob.com')

        self.assertIn('Welcome', mail.outbox[0].subject)

    def test_register_view_post_creates_admin_activated_user(self):
        """register view creates admin activated user on POST"""
        settings.override_setting('account_activation', 'admin')

        response = self.client.post(reverse('misago:register'),
                                    data={'username': 'Bob',
                                          'email': 'bob@bob.com',
                                          'password': 'pass123'})
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('misago:register_completed'))
        self.assertIn('administrator', response.content)

        User = get_user_model()
        user = User.objects.get_by_username('Bob')
        user = User.objects.get_by_email('bob@bob.com')

        self.assertIn('Welcome', mail.outbox[0].subject)
