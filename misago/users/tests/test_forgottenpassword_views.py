from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from misago.users.models import Ban, BAN_USERNAME
from misago.users.testutils import UserTestCase
from misago.users.tokens import make_password_change_token


class ForgottenPasswordViewsTests(UserTestCase):
    def test_guest_request_view_returns_200(self):
        """request new password view returns 200 for guests"""
        response = self.client.get(reverse('misago:forgotten-password'))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_request_view_returns_200(self):
        """request new password view returns 200 for authenticated"""
        self.login_user(self.get_authenticated_user())

        response = self.client.get(reverse('misago:forgotten-password'))
        self.assertEqual(response.status_code, 200)

    def test_change_password_on_banned(self):
        """change banned user password errors"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@test.com', 'Pass.123')

        Ban.objects.create(
            check_type=BAN_USERNAME,
            banned_value='bob',
            user_message='Nope!',
        )

        password_token = make_password_change_token(test_user)

        response = self.client.get(
            reverse('misago:forgotten-password-change-form', kwargs={
                'pk': test_user.pk,
                'token': password_token,
            }))
        self.assertEqual(response.status_code, 403)
        self.assertIn('<p>Nope!</p>', response.content)

    def test_change_password_on_other_user(self):
        """change other user password errors"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@test.com', 'Pass.123')

        password_token = make_password_change_token(test_user)

        self.login_user(self.get_authenticated_user())

        response = self.client.get(
            reverse('misago:forgotten-password-change-form', kwargs={
                'pk': test_user.pk,
                'token': password_token,
            }))
        self.assertEqual(response.status_code, 400)
        self.assertIn('your link has expired', response.content)

    def test_change_password_invalid_token(self):
        """invalid form token errors"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@test.com', 'Pass.123')

        password_token = make_password_change_token(test_user)

        response = self.client.get(
            reverse('misago:forgotten-password-change-form', kwargs={
                'pk': test_user.pk,
                'token': 'abcdfghqsads',
            }))
        self.assertEqual(response.status_code, 400)
        self.assertIn('your link is invalid', response.content)

    def test_change_password_form(self):
        """change user password form displays for valid token"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@test.com', 'Pass.123')

        password_token = make_password_change_token(test_user)

        response = self.client.get(
            reverse('misago:forgotten-password-change-form', kwargs={
                'pk': test_user.pk,
                'token': password_token,
            }))
        self.assertEqual(response.status_code, 200)
        self.assertIn(password_token, response.content)
