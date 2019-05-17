from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...legal.models import Agreement
from ..models import Ban, Online
from ..test import UserTestCase

User = get_user_model()


class UserCreateTests(UserTestCase):
    """tests for new user registration (POST to /api/users/)"""

    def setUp(self):
        super().setUp()

        Agreement.objects.invalidate_cache()

        self.api_link = "/api/users/"

    def tearDown(self):
        Agreement.objects.invalidate_cache()

    def test_empty_request(self):
        """empty request errors with code 400"""
        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "username": ["This field is required."],
                "email": ["This field is required."],
                "password": ["This field is required."],
            },
        )

    def test_invalid_data(self):
        """invalid request data errors with code 400"""
        response = self.client.post(
            self.api_link, "false", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "username": ["This field is required."],
                "email": ["This field is required."],
                "password": ["This field is required."],
            },
        )

    def test_authenticated_request(self):
        """authentiated user request errors with code 403"""
        self.login_user(self.get_authenticated_user())
        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            {"detail": "This action is not available to signed in users."},
        )

    @override_dynamic_settings(account_activation="closed")
    def test_registration_off_request(self):
        """registrations off request errors with code 403"""
        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {"detail": "New users registrations are currently closed."}
        )

    def test_registration_validates_ip_ban(self):
        """api validates ip ban"""
        Ban.objects.create(
            check_type=Ban.IP,
            banned_value="127.*",
            user_message="You can't register account like this.",
        )

        response = self.client.post(
            self.api_link,
            data={
                "username": "totallyNew",
                "email": "loremipsum@dolor.met",
                "password": "LoremP4ssword",
            },
        )

        self.assertEqual(response.status_code, 403)

    def test_registration_validates_ip_registration_ban(self):
        """api validates ip registration-only ban"""
        Ban.objects.create(
            check_type=Ban.IP,
            banned_value="127.*",
            user_message="You can't register account like this.",
            registration_only=True,
        )

        response = self.client.post(
            self.api_link,
            data={
                "username": "totallyNew",
                "email": "loremipsum@dolor.met",
                "password": "LoremP4ssword",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"__all__": ["You can't register account like this."]}
        )

    def test_registration_validates_username(self):
        """api validates usernames"""
        user = self.get_authenticated_user()

        response = self.client.post(
            self.api_link,
            data={
                "username": user.username,
                "email": "loremipsum@dolor.met",
                "password": "LoremP4ssword",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"username": ["This username is not available."]}
        )

    def test_registration_validates_username_ban(self):
        """api validates username ban"""
        Ban.objects.create(
            banned_value="totally*",
            user_message="You can't register account like this.",
        )

        response = self.client.post(
            self.api_link,
            data={
                "username": "totallyNew",
                "email": "loremipsum@dolor.met",
                "password": "LoremP4ssword",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"username": ["You can't register account like this."]}
        )

    def test_registration_validates_username_registration_ban(self):
        """api validates username registration-only ban"""
        Ban.objects.create(
            banned_value="totally*",
            user_message="You can't register account like this.",
            registration_only=True,
        )

        response = self.client.post(
            self.api_link,
            data={
                "username": "totallyNew",
                "email": "loremipsum@dolor.met",
                "password": "LoremP4ssword",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"username": ["You can't register account like this."]}
        )

    def test_registration_validates_email(self):
        """api validates usernames"""
        user = self.get_authenticated_user()

        response = self.client.post(
            self.api_link,
            data={
                "username": "totallyNew",
                "email": user.email,
                "password": "LoremP4ssword",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"email": ["This e-mail address is not available."]}
        )

    def test_registration_validates_email_ban(self):
        """api validates email ban"""
        Ban.objects.create(
            check_type=Ban.EMAIL,
            banned_value="lorem*",
            user_message="You can't register account like this.",
        )

        response = self.client.post(
            self.api_link,
            data={
                "username": "totallyNew",
                "email": "loremipsum@dolor.met",
                "password": "LoremP4ssword",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"email": ["You can't register account like this."]}
        )

    def test_registration_validates_email_registration_ban(self):
        """api validates email registration-only ban"""
        Ban.objects.create(
            check_type=Ban.EMAIL,
            banned_value="lorem*",
            user_message="You can't register account like this.",
            registration_only=True,
        )

        response = self.client.post(
            self.api_link,
            data={
                "username": "totallyNew",
                "email": "loremipsum@dolor.met",
                "password": "LoremP4ssword",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"email": ["You can't register account like this."]}
        )

    def test_registration_requires_password(self):
        """api uses django's validate_password to validate registrations"""
        response = self.client.post(
            self.api_link,
            data={"username": "User", "email": "loremipsum@dolor.met", "password": ""},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"password": ["This field is required."]})

    def test_registration_validates_password(self):
        """api uses django's validate_password to validate registrations"""
        response = self.client.post(
            self.api_link,
            data={
                "username": "User",
                "email": "l.o.r.e.m.i.p.s.u.m@gmail.com",
                "password": "123",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "email": ["This email is not allowed."],
                "password": [
                    (
                        "This password is too short. "
                        "It must contain at least 7 characters."
                    ),
                    "This password is entirely numeric.",
                ],
            },
        )

    def test_registration_validates_password_similiarity(self):
        """api uses validate_password to validate registrations"""
        response = self.client.post(
            self.api_link,
            data={
                "username": "BobBoberson",
                "email": "l.o.r.e.m.i.p.s.u.m@gmail.com",
                "password": "BobBoberson",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "email": ["This email is not allowed."],
                "password": ["The password is too similar to the username."],
            },
        )

    @override_dynamic_settings(
        captcha_type="qa", qa_question="Test", qa_answers="Lorem\nIpsum"
    )
    def test_registration_validates_captcha(self):
        """api validates captcha"""
        response = self.client.post(
            self.api_link,
            data={
                "username": "totallyNew",
                "email": "loremipsum@dolor.met",
                "password": "LoremP4ssword",
                "captcha": "dolor",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"captcha": ["Entered answer is incorrect."]})

        # valid captcha
        response = self.client.post(
            self.api_link,
            data={
                "username": "totallyNew",
                "email": "loremipsum@dolor.met",
                "password": "LoremP4ssword",
                "captcha": "ipSUM",
            },
        )

        self.assertEqual(response.status_code, 200)

    @override_dynamic_settings(
        captcha_type="qa", qa_question="", qa_answers="Lorem\n\nIpsum"
    )
    def test_qacaptcha_handles_empty_answers(self):
        """api validates captcha"""
        response = self.client.post(
            self.api_link,
            data={
                "username": "totallyNew",
                "email": "loremipsum@dolor.met",
                "password": "LoremP4ssword",
                "captcha": "",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"captcha": ["Entered answer is incorrect."]})

    def test_registration_check_agreement(self):
        """api checks agreement"""
        agreement = Agreement.objects.create(
            type=Agreement.TYPE_TOS, text="Lorem ipsum", is_active=True
        )

        response = self.client.post(
            self.api_link,
            data={
                "username": "totallyNew",
                "email": "loremipsum@dolor.met",
                "password": "LoremP4ssword",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"terms_of_service": ["This agreement is required."]}
        )

        # invalid agreement id
        response = self.client.post(
            self.api_link,
            data={
                "username": "totallyNew",
                "email": "loremipsum@dolor.met",
                "password": "LoremP4ssword",
                "terms_of_service": agreement.id + 1,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"terms_of_service": ["This agreement is required."]}
        )

        # valid agreement id
        response = self.client.post(
            self.api_link,
            data={
                "username": "totallyNew",
                "email": "loremipsum@dolor.met",
                "password": "LoremP4ssword",
                "terms_of_service": agreement.id,
            },
        )

        self.assertEqual(response.status_code, 200)

        user = User.objects.get(email="loremipsum@dolor.met")
        self.assertEqual(user.agreements, [agreement.id])
        self.assertEqual(user.useragreement_set.count(), 1)

    def test_registration_ignore_inactive_agreement(self):
        """api ignores inactive agreement"""
        Agreement.objects.create(
            type=Agreement.TYPE_TOS, text="Lorem ipsum", is_active=False
        )

        response = self.client.post(
            self.api_link,
            data={
                "username": "totallyNew",
                "email": "loremipsum@dolor.met",
                "password": "LoremP4ssword",
                "terms_of_service": "",
            },
        )

        self.assertEqual(response.status_code, 200)

        user = User.objects.get(email="loremipsum@dolor.met")
        self.assertEqual(user.agreements, [])
        self.assertEqual(user.useragreement_set.count(), 0)

    def test_registration_calls_validate_new_registration(self):
        """api uses validate_new_registration to validate registrations"""
        response = self.client.post(
            self.api_link,
            data={
                "username": "User",
                "email": "l.o.r.e.m.i.p.s.u.m@gmail.com",
                "password": "pas123",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "email": ["This email is not allowed."],
                "password": [
                    "This password is too short. It must contain at least 7 characters."
                ],
            },
        )

    @override_dynamic_settings(account_activation="none")
    def test_registration_creates_active_user(self):
        """api creates active and signed in user on POST"""
        response = self.client.post(
            self.api_link,
            data={
                "username": "User",
                "email": "user@example.com",
                "password": self.USER_PASSWORD,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"activation": "active", "username": "User", "email": "user@example.com"},
        )

        User.objects.get_by_username("User")

        test_user = User.objects.get_by_email("user@example.com")
        self.assertEqual(Online.objects.filter(user=test_user).count(), 1)

        self.assertTrue(test_user.check_password(self.USER_PASSWORD))

        auth_json = self.client.get(reverse("misago:api:auth")).json()
        self.assertTrue(auth_json["is_authenticated"])
        self.assertEqual(auth_json["username"], "User")

        self.assertIn("Welcome", mail.outbox[0].subject)

        self.assertEqual(test_user.audittrail_set.count(), 1)

    @override_dynamic_settings(account_activation="user")
    def test_registration_creates_inactive_user(self):
        """api creates inactive user on POST"""
        response = self.client.post(
            self.api_link,
            data={
                "username": "User",
                "email": "user@example.com",
                "password": self.USER_PASSWORD,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"activation": "user", "username": "User", "email": "user@example.com"},
        )

        auth_json = self.client.get(reverse("misago:api:auth")).json()
        self.assertFalse(auth_json["is_authenticated"])

        User.objects.get_by_username("User")
        User.objects.get_by_email("user@example.com")

        self.assertIn("Welcome", mail.outbox[0].subject)

    @override_dynamic_settings(account_activation="admin")
    def test_registration_creates_admin_activated_user(self):
        """api creates admin activated user on POST"""
        response = self.client.post(
            self.api_link,
            data={
                "username": "User",
                "email": "user@example.com",
                "password": self.USER_PASSWORD,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"activation": "admin", "username": "User", "email": "user@example.com"},
        )

        auth_json = self.client.get(reverse("misago:api:auth")).json()
        self.assertFalse(auth_json["is_authenticated"])

        User.objects.get_by_username("User")
        User.objects.get_by_email("user@example.com")

        self.assertIn("Welcome", mail.outbox[0].subject)

    @override_dynamic_settings(account_activation="none")
    def test_registration_creates_user_with_whitespace_password(self):
        """api creates user with spaces around password"""
        password = " %s " % self.USER_PASSWORD
        response = self.client.post(
            self.api_link,
            data={
                "username": "User",
                "email": "user@example.com",
                "password": password,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"activation": "active", "username": "User", "email": "user@example.com"},
        )

        User.objects.get_by_username("User")

        test_user = User.objects.get_by_email("user@example.com")
        self.assertEqual(Online.objects.filter(user=test_user).count(), 1)
        self.assertTrue(test_user.check_password(password))

        self.assertIn("Welcome", mail.outbox[0].subject)
