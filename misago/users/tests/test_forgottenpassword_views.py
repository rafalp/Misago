from django.contrib.auth import get_user_model
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

from misago.users.models import Ban, BAN_USERNAME
from misago.users.tokens import make_password_reset_token


class ForgottenPasswordViewsTests(TestCase):
    def test_view_get_returns_200(self):
        """request new password view returns 200 on GET"""
        response = self.client.get(reverse('misago:request_password_reset'))
        self.assertEqual(response.status_code, 200)

    def test_view_submit(self):
        """request new password view sends confirmation mail"""
        User = get_user_model()
        User.objects.create_user('Bob', 'bob@test.com', 'Pass.123')

        response = self.client.post(
            reverse('misago:request_password_reset'),
            data={'username': 'Bob'})

        self.assertEqual(response.status_code, 302)

        self.assertIn('password change', mail.outbox[0].subject)

    def test_view_submit_banned(self):
        """request new password view errors for banned users"""
        User = get_user_model()
        User.objects.create_user('Bob', 'bob@test.com', 'Pass.123')
        Ban.objects.create(test=BAN_USERNAME, banned_value='bob',
                           user_message='Nope!')

        response = self.client.post(
            reverse('misago:request_password_reset'),
            data={'username': 'Bob'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Nope!', response.content)

        self.assertTrue(not mail.outbox)

    def test_view_submit_inactive(self):
        """request new password view errors for inactive users"""
        User = get_user_model()
        User.objects.create_user('Bob', 'bob@test.com', 'Pass.123',
                                 requires_activation=1)

        response = self.client.post(
            reverse('misago:request_password_reset'),
            data={'username': 'Bob'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('activate', response.content)

        self.assertTrue(not mail.outbox)

    def test_change_password_on_banned(self):
        """change banned user password errors"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@test.com', 'Pass.123')
        old_password = test_user.password

        Ban.objects.create(test=BAN_USERNAME, banned_value='bob',
                           user_message='Nope!')

        password_token = make_password_reset_token(test_user)

        response = self.client.get(
            reverse('misago:reset_password_confirm',
                    kwargs={'user_id': test_user.pk,
                            'token': password_token}))
        self.assertEqual(response.status_code, 302)

        test_user = User.objects.get(pk=test_user.pk)
        self.assertEqual(test_user.password, old_password)

        self.assertTrue(not mail.outbox)

    def test_change_password_on_inactive(self):
        """change inactive user password errors"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@test.com', 'Pass.123',
                                             requires_activation=1)
        old_password = test_user.password

        password_token = make_password_reset_token(test_user)

        response = self.client.get(
            reverse('misago:reset_password_confirm',
                    kwargs={'user_id': test_user.pk,
                            'token': password_token}))
        self.assertEqual(response.status_code, 302)

        test_user = User.objects.get(pk=test_user.pk)
        self.assertEqual(test_user.password, old_password)

        self.assertTrue(not mail.outbox)

    def test_successful_change(self):
        """change allright user password"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@test.com', 'Pass.123')
        old_password = test_user.password

        password_token = make_password_reset_token(test_user)

        response = self.client.get(
            reverse('misago:reset_password_confirm',
                    kwargs={'user_id': test_user.pk,
                            'token': password_token}))
        self.assertEqual(response.status_code, 302)

        test_user = User.objects.get(pk=test_user.pk)
        self.assertNotEqual(test_user.password, old_password)

        self.assertIn('New password', mail.outbox[0].subject)
