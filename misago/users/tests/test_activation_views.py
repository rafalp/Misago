from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from misago.core.utils import encode_json_html
from misago.users.models import Ban
from misago.users.tokens import make_activation_token


UserModel = get_user_model()


class ActivationViewsTests(TestCase):
    def test_request_view_returns_200(self):
        """request new activation link view returns 200"""
        response = self.client.get(reverse('misago:request-activation'))
        self.assertEqual(response.status_code, 200)

    def test_view_activate_banned(self):
        """activate banned user shows error"""
        test_user = UserModel.objects.create_user(
            'Bob', 'bob@test.com', 'Pass.123', requires_activation=1
        )
        Ban.objects.create(
            check_type=Ban.USERNAME,
            banned_value='bob',
            user_message='Nope!',
        )

        activation_token = make_activation_token(test_user)

        response = self.client.get(
            reverse(
                'misago:activate-by-token',
                kwargs={
                    'pk': test_user.pk,
                    'token': activation_token,
                }
            )
        )
        self.assertContains(response, encode_json_html("<p>Nope!</p>"), status_code=403)

        test_user = UserModel.objects.get(pk=test_user.pk)
        self.assertEqual(test_user.requires_activation, 1)

    def test_view_activate_invalid_token(self):
        """activate with invalid token shows error"""
        test_user = UserModel.objects.create_user(
            'Bob', 'bob@test.com', 'Pass.123', requires_activation=1
        )

        activation_token = make_activation_token(test_user)

        response = self.client.get(
            reverse(
                'misago:activate-by-token',
                kwargs={
                    'pk': test_user.pk,
                    'token': activation_token + 'acd',
                }
            )
        )
        self.assertEqual(response.status_code, 400)

        test_user = UserModel.objects.get(pk=test_user.pk)
        self.assertEqual(test_user.requires_activation, 1)

    def test_view_activate_disabled(self):
        """activate disabled user shows error"""
        test_user = UserModel.objects.create_user(
            'Bob', 'bob@test.com', 'Pass.123', is_active=False
        )

        activation_token = make_activation_token(test_user)

        response = self.client.get(
            reverse(
                'misago:activate-by-token',
                kwargs={
                    'pk': test_user.pk,
                    'token': activation_token,
                }
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_view_activate_active(self):
        """activate active user shows error"""
        test_user = UserModel.objects.create_user('Bob', 'bob@test.com', 'Pass.123')

        activation_token = make_activation_token(test_user)

        response = self.client.get(
            reverse(
                'misago:activate-by-token',
                kwargs={
                    'pk': test_user.pk,
                    'token': activation_token,
                }
            )
        )
        self.assertEqual(response.status_code, 200)

        test_user = UserModel.objects.get(pk=test_user.pk)
        self.assertEqual(test_user.requires_activation, 0)

    def test_view_activate_inactive(self):
        """activate inactive user passess"""
        test_user = UserModel.objects.create_user(
            'Bob', 'bob@test.com', 'Pass.123', requires_activation=1
        )

        activation_token = make_activation_token(test_user)

        response = self.client.get(
            reverse(
                'misago:activate-by-token',
                kwargs={
                    'pk': test_user.pk,
                    'token': activation_token,
                }
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "your account has been activated!")

        test_user = UserModel.objects.get(pk=test_user.pk)
        self.assertEqual(test_user.requires_activation, 0)
