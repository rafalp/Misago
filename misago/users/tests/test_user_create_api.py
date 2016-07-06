from django.contrib.auth import get_user_model
from django.core import mail
from django.core.urlresolvers import reverse

from misago.conf import settings
from misago.users.models import Online
from misago.users.testutils import UserTestCase


class UserCreateTests(UserTestCase):
    """
    tests for new user registration (POST to /api/users/)
    """
    def test_empty_request(self):
        """empty request errors with code 400"""
        response = self.client.post('/api/users/')
        self.assertEqual(response.status_code, 400)

    def test_authenticated_request(self):
        """authentiated user request errors with code 403"""
        self.login_user(self.get_authenticated_user())
        response = self.client.post('/api/users/')
        self.assertEqual(response.status_code, 403)

    def test_registration_off_request(self):
        """registrations off request errors with code 403"""
        settings.override_setting('account_activation', 'closed')

        response = self.client.post('/api/users/')
        self.assertEqual(response.status_code, 403)
        self.assertIn('closed', response.content)

    def test_registration_creates_active_user(self):
        """api creates active and signed in user on POST"""
        settings.override_setting('account_activation', 'none')

        response = self.client.post('/api/users/',
                                    data={'username': 'Bob',
                                          'email': 'bob@bob.com',
                                          'password': 'pass123'})

        self.assertEqual(response.status_code, 200)
        self.assertIn('active', response.content)
        self.assertIn('Bob', response.content)
        self.assertIn('bob@bob.com', response.content)

        User = get_user_model()
        User.objects.get_by_username('Bob')

        test_user = User.objects.get_by_email('bob@bob.com')
        self.assertEqual(Online.objects.filter(user=test_user).count(), 1)

        response = self.client.get(reverse('misago:index'))
        self.assertIn('Bob', response.content)

        self.assertIn('Welcome', mail.outbox[0].subject)

    def test_registration_creates_inactive_user(self):
        """api creates inactive user on POST"""
        settings.override_setting('account_activation', 'user')

        response = self.client.post('/api/users/',
                                    data={'username': 'Bob',
                                          'email': 'bob@bob.com',
                                          'password': 'pass123'})

        self.assertEqual(response.status_code, 200)
        self.assertIn('user', response.content)
        self.assertIn('Bob', response.content)
        self.assertIn('bob@bob.com', response.content)

        User = get_user_model()
        User.objects.get_by_username('Bob')
        User.objects.get_by_email('bob@bob.com')

        self.assertIn('Welcome', mail.outbox[0].subject)

    def test_registration_creates_admin_activated_user(self):
        """api creates admin activated user on POST"""
        settings.override_setting('account_activation', 'admin')

        response = self.client.post('/api/users/',
                                    data={'username': 'Bob',
                                          'email': 'bob@bob.com',
                                          'password': 'pass123'})

        self.assertEqual(response.status_code, 200)
        self.assertIn('admin', response.content)
        self.assertIn('Bob', response.content)
        self.assertIn('bob@bob.com', response.content)

        User = get_user_model()
        User.objects.get_by_username('Bob')
        User.objects.get_by_email('bob@bob.com')

        self.assertIn('Welcome', mail.outbox[0].subject)
