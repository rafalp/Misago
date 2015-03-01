from django.contrib.auth import get_user_model
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

from misago.users.models import Ban, BAN_USERNAME
from misago.users.tokens import make_password_change_token


class SendLinkAPITests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user('Bob', 'bob@test.com', 'Pass.123')
        self.link = reverse('misago:api:change_password_send_link')

    def test_submit_valid(self):
        """request change password form link api sends reset link mail"""
        response = self.client.post(self.link, data={'email': self.user.email})
        self.assertEqual(response.status_code, 200)

        self.assertIn('Change Bob password', mail.outbox[0].subject)

    def test_submit_invalid(self):
        """request change password form link api errors for invalid email"""
        response = self.client.post(self.link, data={'email': 'fake@mail.com'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('not_found', response.content)

        self.assertTrue(not mail.outbox)

    def test_submit_banned(self):
        """request change password form link api errors for banned users"""
        Ban.objects.create(check_type=BAN_USERNAME,
                           banned_value=self.user.username,
                           user_message='Nope!')

        response = self.client.post(self.link, data={'email': self.user.email})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Nope!', response.content)

        self.assertTrue(not mail.outbox)

    def test_view_submit_inactive_user(self):
        """request change password form link api errors for inactive users"""
        self.user.requires_activation = 1
        self.user.save()

        response = self.client.post(self.link, data={'email': self.user.email})
        self.assertEqual(response.status_code, 400)
        self.assertIn('inactive_user', response.content)

        self.user.requires_activation = 2
        self.user.save()

        response = self.client.post(self.link, data={'email': self.user.email})
        self.assertEqual(response.status_code, 400)
        self.assertIn('inactive_admin', response.content)

        self.assertTrue(not mail.outbox)


class ValidateTokenAPITests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user('Bob', 'bob@test.com', 'Pass.123')
        self.link = reverse(
            'misago:api:change_password_validate_token',
            kwargs={
                'user_id': self.user.id,
                'token': make_password_change_token(self.user)
            })

    def test_submit_valid(self):
        """validate form link api returns success"""
        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user.username, response.content)

    def test_submit_invalid_token(self):
        """validate form link api errors for invalid token"""
        response = self.client.post(reverse(
            'misago:api:change_password_validate_token',
            kwargs={
                'user_id': self.user.id,
                'token': 'sadsadsadsdsassdsa'
            }))
        self.assertEqual(response.status_code, 404)
        self.assertIn('Your link is invalid.', response.content)

    def test_submit_invalid_user(self):
        """validate form link api errors for invalid user"""
        response = self.client.post(reverse(
            'misago:api:change_password_validate_token',
            kwargs={
                'user_id': 123,
                'token': 'sadsadsadsdsassdsa'
            }))
        self.assertEqual(response.status_code, 404)

    def test_submit_banned(self):
        """validate form link api errors for banned user"""
        Ban.objects.create(check_type=BAN_USERNAME,
                           banned_value=self.user.username,
                           user_message='Nope!')

        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 404)
        self.assertIn('Your link has expired.', response.content)

    def test_view_submit_inactive_user(self):
        """validate form link api errors for inactive user"""
        self.user.requires_activation = 1
        self.user.save()

        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 404)
        self.assertIn('Your link has expired.', response.content)

        self.user.requires_activation = 2
        self.user.save()

        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 404)
        self.assertIn('Your link has expired.', response.content)


class ChangePasswordAPITests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user('Bob', 'bob@test.com', 'Pass.123')
        self.link = reverse(
            'misago:api:change_password',
            kwargs={
                'user_id': self.user.id,
                'token': make_password_change_token(self.user)
            })

    def test_submit_valid(self):
        """change password api changes user password"""
        response = self.client.post(self.link, data={'password': 'newpass'})
        self.assertEqual(response.status_code, 200)

        user = get_user_model().objects.get(id=self.user.id)
        self.assertTrue(user.check_password('newpass'))

    def test_submit_invalid_empty(self):
        """change password api errors for unvalid password"""
        response = self.client.post(self.link, data={'password': ''})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Valid password must be', response.content)

    def test_submit_invalid_token(self):
        """change password api errors for unvalid token"""
        response = self.client.post(reverse('misago:api:change_password',
            kwargs={
                'user_id': self.user.id,
                'token': 'sadsadsadsdsassdsa'
            }),
            data={'password': 'newpass'})
        self.assertEqual(response.status_code, 404)
        self.assertIn('Your link is invalid.', response.content)

    def test_submit_invalid_user(self):
        """validate form link api errors for invalid user"""
        response = self.client.post(reverse('misago:api:change_password',
            kwargs={
                'user_id': 123,
                'token': 'sadsadsadsdsassdsa'
            }),
            data={'password': 'newpass'})
        self.assertEqual(response.status_code, 404)

    def test_submit_banned(self):
        """validate form link api errors for banned user"""
        Ban.objects.create(check_type=BAN_USERNAME,
                           banned_value=self.user.username,
                           user_message='Nope!')

        response = self.client.post(self.link, data={'password': 'newpass'})
        self.assertEqual(response.status_code, 404)
        self.assertIn('Your link has expired.', response.content)

    def test_view_submit_inactive_user(self):
        """validate form link api errors for inactive user"""
        self.user.requires_activation = 1
        self.user.save()

        response = self.client.post(self.link, data={'password': 'newpass'})
        self.assertEqual(response.status_code, 404)
        self.assertIn('Your link has expired.', response.content)

        self.user.requires_activation = 2
        self.user.save()

        response = self.client.post(self.link, data={'password': 'newpass'})
        self.assertEqual(response.status_code, 404)
        self.assertIn('Your link has expired.', response.content)
