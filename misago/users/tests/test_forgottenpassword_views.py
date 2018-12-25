from django.urls import reverse

from ...core.utils import encode_json_html
from ..models import Ban
from ..test import UserTestCase, create_test_user
from ..tokens import make_password_change_token


class ForgottenPasswordViewsTests(UserTestCase):
    def test_guest_request_view_returns_200(self):
        """request new password view returns 200 for guests"""
        response = self.client.get(reverse("misago:forgotten-password"))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_request_view_returns_200(self):
        """request new password view returns 200 for authenticated"""
        self.login_user(self.get_authenticated_user())

        response = self.client.get(reverse("misago:forgotten-password"))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_request_unusable_password_view_returns_200(self):
        """
        request new password view returns 200 for authenticated with unusable password
        """
        user = self.get_authenticated_user()
        user.set_password(None)
        user.save()

        self.assertFalse(user.has_usable_password())
        self.login_user(user)

        response = self.client.get(reverse("misago:forgotten-password"))
        self.assertEqual(response.status_code, 200)

    def test_change_password_on_banned(self):
        """change banned user password errors"""
        user = create_test_user(
            "OtherUser", "otheruser@example.com", self.USER_PASSWORD
        )

        Ban.objects.create(
            check_type=Ban.USERNAME, banned_value="OtherUser", user_message="Nope!"
        )

        password_token = make_password_change_token(user)

        response = self.client.get(
            reverse(
                "misago:forgotten-password-change-form",
                kwargs={"pk": user.pk, "token": password_token},
            )
        )
        self.assertContains(response, encode_json_html("<p>Nope!</p>"), status_code=403)

    def test_change_password_on_other_user(self):
        """change other user password errors"""
        user = create_test_user(
            "OtherUser", "otheruser@example.com", self.USER_PASSWORD
        )

        password_token = make_password_change_token(user)

        self.login_user(self.get_authenticated_user())

        response = self.client.get(
            reverse(
                "misago:forgotten-password-change-form",
                kwargs={"pk": user.pk, "token": password_token},
            )
        )
        self.assertContains(response, "your link has expired", status_code=400)

    def test_change_password_invalid_token(self):
        """invalid form token errors"""
        user = create_test_user(
            "OtherUser", "otheruser@example.com", self.USER_PASSWORD
        )

        response = self.client.get(
            reverse(
                "misago:forgotten-password-change-form",
                kwargs={"pk": user.pk, "token": "abcdfghqsads"},
            )
        )
        self.assertContains(response, "your link is invalid", status_code=400)

    def test_change_password_form(self):
        """change user password form displays for valid token"""
        user = create_test_user(
            "OtherUser", "otheruser@example.com", self.USER_PASSWORD
        )

        password_token = make_password_change_token(user)

        response = self.client.get(
            reverse(
                "misago:forgotten-password-change-form",
                kwargs={"pk": user.pk, "token": password_token},
            )
        )
        self.assertContains(response, password_token)

    def test_change_password_unusable_password_form(self):
        """set user first password form displays for valid token"""
        user = create_test_user("OtherUser", "otheruser@example.com")

        password_token = make_password_change_token(user)

        response = self.client.get(
            reverse(
                "misago:forgotten-password-change-form",
                kwargs={"pk": user.pk, "token": password_token},
            )
        )
        self.assertContains(response, password_token)
