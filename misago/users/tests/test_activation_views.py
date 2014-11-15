from django.contrib.auth import get_user_model
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

from misago.users.models import Ban, BAN_USERNAME
from misago.users.tokens import make_activation_token


class ActivationViewsTests(TestCase):
    def test_view_get_returns_200(self):
        """request activation view returns 200 on GET"""
        response = self.client.get(reverse('misago:request_activation'))
        self.assertEqual(response.status_code, 200)

    def test_view_submit(self):
        """request activation view sends mail"""
        User = get_user_model()
        User.objects.create_user('Bob', 'bob@test.com', 'Pass.123',
                                 requires_activation=1)

        response = self.client.post(
            reverse('misago:request_activation'),
            data={'username': 'Bob'})

        self.assertEqual(response.status_code, 302)

        self.assertIn('Account activation', mail.outbox[0].subject)

    def test_view_submit_banned(self):
        """request activation for banned shows error"""
        User = get_user_model()
        User.objects.create_user('Bob', 'bob@test.com', 'Pass.123',
                                 requires_activation=1)
        Ban.objects.create(check_type=BAN_USERNAME,
                           banned_value='bob',
                           user_message='Nope!')

        response = self.client.post(
            reverse('misago:request_activation'),
            data={'username': 'Bob'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Nope!', response.content)

        self.assertTrue(not mail.outbox)

    def test_view_submit_active(self):
        """request activation for active shows error"""
        User = get_user_model()
        User.objects.create_user('Bob', 'bob@test.com', 'Pass.123')

        response = self.client.post(
            reverse('misago:request_activation'),
            data={'username': 'Bob'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('already active', response.content)

        self.assertTrue(not mail.outbox)

    def test_view_activate_banned(self):
        """activate banned user shows error"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@test.com', 'Pass.123',
                                             requires_activation=1)
        Ban.objects.create(check_type=BAN_USERNAME,
                           banned_value='bob',
                           user_message='Nope!')

        activation_token = make_activation_token(test_user)

        response = self.client.get(
            reverse('misago:activate_by_token',
                    kwargs={'user_id': test_user.pk,
                            'token': activation_token}))
        self.assertEqual(response.status_code, 302)

        test_user = User.objects.get(pk=test_user.pk)
        self.assertEqual(test_user.requires_activation, 1)

    def test_view_activate_active(self):
        """activate active user shows error"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@test.com', 'Pass.123')

        activation_token = make_activation_token(test_user)

        response = self.client.get(
            reverse('misago:activate_by_token',
                    kwargs={'user_id': test_user.pk,
                            'token': activation_token}))
        self.assertEqual(response.status_code, 302)

        test_user = User.objects.get(pk=test_user.pk)
        self.assertEqual(test_user.requires_activation, 0)

    def test_view_activate_inactive(self):
        """activate inactive user passess"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@test.com', 'Pass.123',
                                             requires_activation=1)

        activation_token = make_activation_token(test_user)

        response = self.client.get(
            reverse('misago:activate_by_token',
                    kwargs={'user_id': test_user.pk,
                            'token': activation_token}))
        self.assertEqual(response.status_code, 302)

        test_user = User.objects.get(pk=test_user.pk)
        self.assertEqual(test_user.requires_activation, 0)
