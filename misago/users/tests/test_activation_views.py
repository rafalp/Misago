from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ...core.utils import encode_json_html
from ..models import Ban
from ..test import create_test_user
from ..tokens import make_activation_token

User = get_user_model()


class ActivationViewsTests(TestCase):
    def test_request_view_returns_200(self):
        """request new activation link view returns 200"""
        response = self.client.get(reverse("misago:request-activation"))
        self.assertEqual(response.status_code, 200)

    def test_view_activate_banned(self):
        """activate banned user shows error"""
        user = create_test_user("User", "user@example.com", requires_activation=1)
        activation_token = make_activation_token(user)

        Ban.objects.create(
            check_type=Ban.USERNAME, banned_value="user", user_message="Nope!"
        )

        response = self.client.get(
            reverse(
                "misago:activate-by-token",
                kwargs={"pk": user.pk, "token": activation_token},
            )
        )
        self.assertContains(response, encode_json_html("<p>Nope!</p>"), status_code=403)

        user = User.objects.get(pk=user.pk)
        self.assertEqual(user.requires_activation, 1)

    def test_view_activate_invalid_token(self):
        """activate with invalid token shows error"""
        user = create_test_user("User", "user@example.com", requires_activation=1)
        activation_token = make_activation_token(user)

        response = self.client.get(
            reverse(
                "misago:activate-by-token",
                kwargs={"pk": user.pk, "token": activation_token + "acd"},
            )
        )
        self.assertEqual(response.status_code, 400)

        user = User.objects.get(pk=user.pk)
        self.assertEqual(user.requires_activation, 1)

    def test_view_activate_disabled(self):
        """activate disabled user shows error"""
        user = create_test_user("User", "user@example.com", is_active=False)
        activation_token = make_activation_token(user)

        response = self.client.get(
            reverse(
                "misago:activate-by-token",
                kwargs={"pk": user.pk, "token": activation_token},
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_view_activate_active(self):
        """activate active user shows error"""
        user = create_test_user("User", "user@example.com")
        activation_token = make_activation_token(user)

        response = self.client.get(
            reverse(
                "misago:activate-by-token",
                kwargs={"pk": user.pk, "token": activation_token},
            )
        )
        self.assertEqual(response.status_code, 200)

        user = User.objects.get(pk=user.pk)
        self.assertEqual(user.requires_activation, 0)

    def test_view_activate_inactive(self):
        """activate inactive user passess"""
        user = create_test_user("User", "user@example.com", requires_activation=1)
        activation_token = make_activation_token(user)

        response = self.client.get(
            reverse(
                "misago:activate-by-token",
                kwargs={"pk": user.pk, "token": activation_token},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "your account has been activated!")

        user = User.objects.get(pk=user.pk)
        self.assertEqual(user.requires_activation, 0)
