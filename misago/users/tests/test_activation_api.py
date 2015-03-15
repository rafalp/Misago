from django.contrib.auth import get_user_model
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

from misago.users.models import Ban, BAN_USERNAME
from misago.users.tokens import make_activation_token


class SendLinkAPITests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user('Bob', 'bob@test.com', 'Pass.123')
        self.user.requires_activation = 1
        self.user.save()

        self.link = reverse('misago:api:activation_send_link')

    def test_submit_valid(self):
        """request activation link api sends reset link mail"""
        response = self.client.post(self.link, data={'email': self.user.email})
        self.assertEqual(response.status_code, 200)

        self.assertIn('Change Bob password', mail.outbox[0].subject)

    def test_submit_invalid(self):
        """request activation link api errors for invalid email"""
        response = self.client.post(self.link, data={'email': 'fake@mail.com'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('not_found', response.content)

        self.assertTrue(not mail.outbox)

    def test_submit_banned(self):
        """request activation link api errors for banned users"""
        Ban.objects.create(check_type=BAN_USERNAME,
                           banned_value=self.user.username,
                           user_message='Nope!')

        response = self.client.post(self.link, data={'email': self.user.email})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Nope!', response.content)

        self.assertTrue(not mail.outbox)

    def test_view_submit_active_user(self):
        """request activation link api errors for active user"""
        self.user.requires_activation = 0
        self.user.save()

        response = self.client.post(self.link, data={'email': self.user.email})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Bob, your account is already activated.',
                      response.content)

    def test_view_submit_inactive_user(self):
        """request activation link api errors for admin-activated users"""
        self.user.requires_activation = 2
        self.user.save()

        response = self.client.post(self.link, data={'email': self.user.email})
        self.assertEqual(response.status_code, 400)
        self.assertIn('inactive_admin', response.content)

        self.assertTrue(not mail.outbox)

        # but succeed for user-activated
        self.user.requires_activation = 1
        self.user.save()

        response = self.client.post(self.link, data={'email': self.user.email})
        self.assertEqual(response.status_code, 200)

        self.assertTrue(mail.outbox)


class ValidateTokenAPITests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user('Bob', 'bob@test.com', 'Pass.123')
        self.user.requires_activation = 1
        self.user.save()

        self.link = reverse(
            'misago:api:activation_validate_token',
            kwargs={
                'user_id': self.user.id,
                'token': make_activation_token(self.user)
            })

    def test_submit_valid(self):
        """validate link api returns success and activates user"""
        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user.username, response.content)

        user = get_user_model().objects.get(id=self.user.id)
        self.assertFalse(user.requires_activation)

    def test_submit_invalid_token(self):
        """validate link api errors for invalid token"""
        response = self.client.post(reverse(
            'misago:api:activation_validate_token',
            kwargs={
                'user_id': self.user.id,
                'token': 'sadsadsadsdsassdsa'
            }))
        self.assertEqual(response.status_code, 404)
        self.assertIn('Your link is invalid.', response.content)

    def test_submit_invalid_user(self):
        """validate link api errors for invalid user"""
        response = self.client.post(reverse(
            'misago:api:activation_validate_token',
            kwargs={
                'user_id': 123,
                'token': 'sadsadsadsdsassdsa'
            }))
        self.assertEqual(response.status_code, 404)

    def test_submit_banned(self):
        """validate link api errors for banned user"""
        Ban.objects.create(check_type=BAN_USERNAME,
                           banned_value=self.user.username,
                           user_message='Nope!')

        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 404)
        self.assertIn('Your link has expired.', response.content)

    def test_view_submit_active_user(self):
        """validate link api errors for active user"""
        self.user.requires_activation = 0
        self.user.save()

        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 404)
        self.assertIn('Bob, your account is already activated.',
                      response.content)

    def test_view_submit_inactive_user(self):
        """validate link api errors for inactive user"""
        self.user.requires_activation = 1
        self.user.save()

        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 200)

        self.user.requires_activation = 2
        self.user.save()

        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 404)
        self.assertIn('Bob, only administrator may activate your account.',
                      response.content)
