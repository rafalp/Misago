from django.core import mail
from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ..test import AuthenticatedUserTestCase, create_test_user


class UserChangeEmailTests(AuthenticatedUserTestCase):
    """tests for user change email RPC (/api/users/1/change-email/)"""

    def setUp(self):
        super().setUp()
        self.link = "/api/users/%s/change-email/" % self.user.pk

    def test_unsupported_methods(self):
        """api isn't supporting GET"""
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 405)

    def test_empty_input(self):
        """api errors correctly for empty input"""
        response = self.client.post(self.link, data={})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "new_email": ["This field is required."],
                "password": ["This field is required."],
            },
        )

    def test_invalid_password(self):
        """api errors correctly for invalid password"""
        response = self.client.post(
            self.link, data={"new_email": "new@email.com", "password": "Lor3mIpsum"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"password": ["Entered password is invalid."]}
        )

    def test_invalid_input(self):
        """api errors correctly for invalid input"""
        response = self.client.post(
            self.link, data={"new_email": "", "password": self.USER_PASSWORD}
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"new_email": ["This field may not be blank."]}
        )

        response = self.client.post(
            self.link, data={"new_email": "newmail", "password": self.USER_PASSWORD}
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"new_email": ["Enter a valid email address."]}
        )

    def test_email_taken(self):
        """api validates email usage"""
        taken_email = "otheruser@example.com"
        create_test_user("OtherUser", taken_email)

        response = self.client.post(
            self.link, data={"new_email": taken_email, "password": self.USER_PASSWORD}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"new_email": ["This e-mail address is not available."]}
        )

    @override_dynamic_settings(forum_address="http://test.com/")
    def test_change_email(self):
        """api allows users to change their e-mail addresses"""
        new_email = "new@email.com"

        response = self.client.post(
            self.link, data={"new_email": new_email, "password": self.USER_PASSWORD}
        )
        self.assertEqual(response.status_code, 200)

        self.assertIn("Confirm e-mail change", mail.outbox[0].subject)
        for line in [l.strip() for l in mail.outbox[0].body.splitlines()]:
            if line.startswith("http://"):
                token = line.rstrip("/").split("/")[-1]
                break
        else:
            self.fail("E-mail sent didn't contain confirmation url")

        response = self.client.get(
            reverse("misago:options-confirm-email-change", kwargs={"token": token})
        )

        self.assertEqual(response.status_code, 200)

        self.reload_user()
        self.assertEqual(self.user.email, new_email)

    @override_dynamic_settings(forum_address="http://test.com/")
    def test_change_email_user_password_whitespace(self):
        """api supports users with whitespace around their passwords"""
        user_password = " old password "
        new_email = "new@email.com"

        self.user.set_password(user_password)
        self.user.save()

        self.login_user(self.user)

        response = self.client.post(
            self.link, data={"new_email": new_email, "password": user_password}
        )
        self.assertEqual(response.status_code, 200)

        self.assertIn("Confirm e-mail change", mail.outbox[0].subject)
        for line in [l.strip() for l in mail.outbox[0].body.splitlines()]:
            if line.startswith("http://"):
                token = line.rstrip("/").split("/")[-1]
                break
        else:
            self.fail("E-mail sent didn't contain confirmation url")

        response = self.client.get(
            reverse("misago:options-confirm-email-change", kwargs={"token": token})
        )

        self.assertEqual(response.status_code, 200)

        self.reload_user()
        self.assertEqual(self.user.email, new_email)

    @override_dynamic_settings(
        enable_oauth2_client=True,
        oauth2_provider="Lorem",
    )
    def test_change_email_api_returns_403_if_oauth_is_enabled(self):
        new_email = "new@email.com"

        self.login_user(self.user)

        response = self.client.post(
            self.link, data={"new_email": new_email, "password": self.USER_PASSWORD}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(len(mail.outbox), 0)

    @override_dynamic_settings(forum_address="http://test.com/")
    def test_confirm_change_email_view_returns_403_if_oauth_is_enabled(self):
        new_email = "new@email.com"

        self.login_user(self.user)

        response = self.client.post(
            self.link, data={"new_email": new_email, "password": self.USER_PASSWORD}
        )
        self.assertEqual(response.status_code, 200)

        self.assertIn("Confirm e-mail change", mail.outbox[0].subject)
        for line in [l.strip() for l in mail.outbox[0].body.splitlines()]:
            if line.startswith("http://"):
                token = line.rstrip("/").split("/")[-1]
                break
        else:
            self.fail("E-mail sent didn't contain confirmation url")

        with override_dynamic_settings(
            enable_oauth2_client=True, oauth2_provider="Lorem"
        ):
            response = self.client.get(
                reverse("misago:options-confirm-email-change", kwargs={"token": token})
            )

            self.assertEqual(response.status_code, 403)
