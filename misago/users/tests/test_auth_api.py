from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase

from misago.users.models import Ban
from misago.users.tokens import make_password_change_token


UserModel = get_user_model()


class GatewayTests(TestCase):
    def test_api_invalid_credentials(self):
        """login api returns 400 on invalid POST"""
        response = self.client.post(
            "/api/auth/", data={"username": "nope", "password": "nope"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"code": "invalid_login", "detail": "Login or password is incorrect."},
        )

        response = self.client.get("/api/auth/")
        self.assertEqual(response.status_code, 200)

        user_json = response.json()
        self.assertIsNone(user_json["id"])

    def test_login(self):
        """api signs user in"""
        user = UserModel.objects.create_user("Bob", "bob@test.com", "Pass.123")

        response = self.client.post(
            "/api/auth/", data={"username": "Bob", "password": "Pass.123"}
        )

        self.assertEqual(response.status_code, 200)

        response = self.client.get("/api/auth/")
        self.assertEqual(response.status_code, 200)

        user_json = response.json()
        self.assertEqual(user_json["id"], user.id)
        self.assertEqual(user_json["username"], user.username)

    def test_login_whitespaces_password(self):
        """api signs user in with password left untouched"""
        user = UserModel.objects.create_user("Bob", "bob@test.com", " Pass.123 ")

        response = self.client.post(
            "/api/auth/", data={"username": "Bob", "password": "Pass.123"}
        )

        self.assertEqual(response.status_code, 400)

        response = self.client.post(
            "/api/auth/", data={"username": "Bob", "password": " Pass.123 "}
        )

        self.assertEqual(response.status_code, 200)

        response = self.client.get("/api/auth/")
        self.assertEqual(response.status_code, 200)

        user_json = response.json()
        self.assertEqual(user_json["id"], user.id)
        self.assertEqual(user_json["username"], user.username)

    def test_submit_empty(self):
        """login api errors for no body"""
        response = self.client.post("/api/auth/")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"code": "empty_data", "detail": "Fill out both fields."}
        )

    def test_submit_invalid(self):
        """login api errors for invalid data"""
        response = self.client.post(
            "/api/auth/", "false", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "Invalid data. Expected a dictionary, but got bool."
                ]
            },
        )

    def test_login_not_usable_password(self):
        """login api fails to sign user with not-usable password in"""
        UserModel.objects.create_user("Bob", "bob@test.com")

        response = self.client.post(
            "/api/auth/", data={"username": "Bob", "password": "Pass.123"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"code": "invalid_login", "detail": "Login or password is incorrect."},
        )

    def test_login_banned(self):
        """login api fails to sign banned user in"""
        UserModel.objects.create_user("Bob", "bob@test.com", "Pass.123")

        ban = Ban.objects.create(
            check_type=Ban.USERNAME,
            banned_value="bob",
            user_message="You are tragically banned.",
        )

        response = self.client.post(
            "/api/auth/", data={"username": "Bob", "password": "Pass.123"}
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(response_json["code"], "banned")
        self.assertEqual(response_json["detail"]["message"]["plain"], ban.user_message)
        self.assertEqual(
            response_json["detail"]["message"]["html"], "<p>%s</p>" % ban.user_message
        )

        response = self.client.get("/api/auth/")
        self.assertEqual(response.status_code, 200)

        user_json = response.json()
        self.assertIsNone(user_json["id"])

    def test_login_banned_staff(self):
        """login api signs banned staff member in"""
        user = UserModel.objects.create_user("Bob", "bob@test.com", "Pass.123")

        user.is_staff = True
        user.save()

        Ban.objects.create(
            check_type=Ban.USERNAME,
            banned_value="bob",
            user_message="You are tragically banned.",
        )

        response = self.client.post(
            "/api/auth/", data={"username": "Bob", "password": "Pass.123"}
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/api/auth/")
        self.assertEqual(response.status_code, 200)

        user_json = response.json()
        self.assertEqual(user_json["id"], user.id)
        self.assertEqual(user_json["username"], user.username)

    def test_login_ban_registration_only(self):
        """login api ignores registration-only bans"""
        user = UserModel.objects.create_user("Bob", "bob@test.com", "Pass.123")

        Ban.objects.create(
            check_type=Ban.USERNAME, banned_value="bob", registration_only=True
        )

        response = self.client.post(
            "/api/auth/", data={"username": "Bob", "password": "Pass.123"}
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/api/auth/")
        self.assertEqual(response.status_code, 200)

        user_json = response.json()
        self.assertEqual(user_json["id"], user.id)
        self.assertEqual(user_json["username"], user.username)

    def test_login_inactive_admin(self):
        """login api fails to sign admin-activated user in"""
        UserModel.objects.create_user(
            "Bob", "bob@test.com", "Pass.123", requires_activation=1
        )

        response = self.client.post(
            "/api/auth/", data={"username": "Bob", "password": "Pass.123"}
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(response_json["code"], "inactive_user")

        response = self.client.get("/api/auth/")
        self.assertEqual(response.status_code, 200)

        user_json = response.json()
        self.assertIsNone(user_json["id"])

    def test_login_inactive_user(self):
        """login api fails to sign user-activated user in"""
        UserModel.objects.create_user(
            "Bob", "bob@test.com", "Pass.123", requires_activation=2
        )

        response = self.client.post(
            "/api/auth/", data={"username": "Bob", "password": "Pass.123"}
        )
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertEqual(response_json["code"], "inactive_admin")

        response = self.client.get("/api/auth/")
        self.assertEqual(response.status_code, 200)

        user_json = response.json()
        self.assertIsNone(user_json["id"])

    def test_login_disabled_user(self):
        """its impossible to sign in to disabled account"""
        user = UserModel.objects.create_user(
            "Bob", "bob@test.com", "Pass.123", is_active=False
        )

        user.is_staff = True
        user.save()

        response = self.client.post(
            "/api/auth/", data={"username": "Bob", "password": "Pass.123"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"code": "invalid_login", "detail": "Login or password is incorrect."},
        )

        response = self.client.get("/api/auth/")
        self.assertEqual(response.status_code, 200)

        user_json = response.json()
        self.assertIsNone(user_json["id"])


class UserCredentialsTests(TestCase):
    def test_edge_returns_response(self):
        """api edge has no showstoppers"""
        response = self.client.get("/api/auth/criteria/")
        self.assertEqual(response.status_code, 200)


class SendActivationApiTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user("Bob", "bob@test.com", "Pass.123")
        self.user.requires_activation = 1
        self.user.save()

        self.link = "/api/auth/send-activation/"

    def test_submit_valid(self):
        """request activation link api sends reset link mail"""
        response = self.client.post(self.link, data={"email": self.user.email})
        self.assertEqual(response.status_code, 200)

        self.assertIn("Activate Bob", mail.outbox[0].subject)

    def test_submit_banned(self):
        """request activation link api passes for banned users"""
        Ban.objects.create(
            check_type=Ban.USERNAME,
            banned_value=self.user.username,
            user_message="Nope!",
        )

        response = self.client.post(self.link, data={"email": self.user.email})
        self.assertEqual(response.status_code, 200)

        self.assertIn("Activate Bob", mail.outbox[0].subject)

    def test_submit_disabled(self):
        """request activation link api fails disabled users"""
        self.user.is_active = False
        self.user.save()

        response = self.client.post(self.link, data={"email": self.user.email})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"code": "not_found", "detail": "No user with this e-mail exists."},
        )

        self.assertTrue(not mail.outbox)

    def test_submit_empty(self):
        """request activation link api errors for no body"""
        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"code": "empty_email", "detail": "Enter e-mail address."}
        )

        self.assertTrue(not mail.outbox)

    def test_submit_invalid_data(self):
        """login api errors for invalid data"""
        response = self.client.post(self.link, "false", content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "Invalid data. Expected a dictionary, but got bool."
                ]
            },
        )

    def test_submit_invalid_email(self):
        """request activation link api errors for invalid email"""
        response = self.client.post(self.link, data={"email": "fake@mail.com"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"code": "not_found", "detail": "No user with this e-mail exists."},
        )

        self.assertTrue(not mail.outbox)

    def test_submit_active_user(self):
        """request activation link api errors for active user"""
        self.user.requires_activation = 0
        self.user.save()

        response = self.client.post(self.link, data={"email": self.user.email})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "code": "already_active",
                "detail": "Bob, your account is already active.",
            },
        )

    def test_submit_inactive_user(self):
        """request activation link api errors for admin-activated users"""
        self.user.requires_activation = 2
        self.user.save()

        response = self.client.post(self.link, data={"email": self.user.email})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "code": "inactive_admin",
                "detail": "Bob, only administrator may activate your account.",
            },
        )

        self.assertTrue(not mail.outbox)

        # but succeed for user-activated
        self.user.requires_activation = 1
        self.user.save()

        response = self.client.post(self.link, data={"email": self.user.email})
        self.assertEqual(response.status_code, 200)

        self.assertTrue(mail.outbox)


class SendPasswordFormApiTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user("Bob", "bob@test.com", "Pass.123")

        self.link = "/api/auth/send-password-form/"

    def test_submit_valid(self):
        """request change password form link api sends reset link mail"""
        response = self.client.post(self.link, data={"email": self.user.email})
        self.assertEqual(response.status_code, 200)

        self.assertIn("Change Bob password", mail.outbox[0].subject)

    def test_submit_banned(self):
        """request change password form link api sends reset link mail"""
        Ban.objects.create(
            check_type=Ban.USERNAME,
            banned_value=self.user.username,
            user_message="Nope!",
        )

        response = self.client.post(self.link, data={"email": self.user.email})
        self.assertEqual(response.status_code, 200)

        self.assertIn("Change Bob password", mail.outbox[0].subject)

    def test_submit_disabled(self):
        """request change password form api fails disabled users"""
        self.user.is_active = False
        self.user.save()

        response = self.client.post(self.link, data={"email": self.user.email})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"code": "not_found", "detail": "No user with this e-mail exists."},
        )

        self.assertTrue(not mail.outbox)

    def test_submit_empty(self):
        """request change password form link api errors for no body"""
        response = self.client.post(self.link)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"code": "empty_email", "detail": "Enter e-mail address."}
        )

        self.assertTrue(not mail.outbox)

    def test_submit_invalid(self):
        """request change password form link api errors for invalid email"""
        response = self.client.post(self.link, data={"email": "fake@mail.com"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"code": "not_found", "detail": "No user with this e-mail exists."},
        )

        self.assertTrue(not mail.outbox)

    def test_submit_invalid_data(self):
        """login api errors for invalid data"""
        response = self.client.post(self.link, "false", content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "Invalid data. Expected a dictionary, but got bool."
                ]
            },
        )

    def test_submit_inactive_user(self):
        """request change password form link api errors for inactive users"""
        self.user.requires_activation = 1
        self.user.save()

        response = self.client.post(self.link, data={"email": self.user.email})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "code": "inactive_user",
                "detail": (
                    "You have to activate your account before you "
                    "will be able to request new password."
                ),
            },
        )

        self.user.requires_activation = 2
        self.user.save()

        response = self.client.post(self.link, data={"email": self.user.email})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "code": "inactive_admin",
                "detail": (
                    "Administrator has to activate your account before you "
                    "will be able to request new password."
                ),
            },
        )

        self.assertTrue(not mail.outbox)


class ChangePasswordApiTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user("Bob", "bob@test.com", "Pass.123")

        self.link = "/api/auth/change-password/%s/%s/"

    def test_submit_valid(self):
        """submit change password form api changes password"""
        response = self.client.post(
            self.link % (self.user.pk, make_password_change_token(self.user)),
            data={"password": "n3wp4ss!"},
        )
        self.assertEqual(response.status_code, 200)

        user = UserModel.objects.get(id=self.user.pk)
        self.assertTrue(user.check_password("n3wp4ss!"))

    def test_submit_with_whitespaces(self):
        """submit change password form api changes password with whitespaces"""
        response = self.client.post(
            self.link % (self.user.pk, make_password_change_token(self.user)),
            data={"password": " n3wp4ss! "},
        )
        self.assertEqual(response.status_code, 200)

        user = UserModel.objects.get(id=self.user.pk)
        self.assertTrue(user.check_password(" n3wp4ss! "))

    def test_submit_invalid_data(self):
        """login api errors for invalid data"""
        response = self.client.post(
            self.link % (self.user.pk, make_password_change_token(self.user)),
            "false",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "Invalid data. Expected a dictionary, but got bool."
                ]
            },
        )

    def test_invalid_token_link(self):
        """api errors on invalid user id link"""
        response = self.client.post(self.link % (self.user.pk, "asda7ad89sa7d9s789as"))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"detail": "Form link is invalid. Please try again."}
        )

    def test_banned_user_link(self):
        """request errors because user is banned"""
        Ban.objects.create(
            check_type=Ban.USERNAME,
            banned_value=self.user.username,
            user_message="Nope!",
        )

        response = self.client.post(
            self.link % (self.user.pk, make_password_change_token(self.user))
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "Your link has expired. Please request new one."},
        )

    def test_inactive_user(self):
        """change password api errors for inactive users"""
        self.user.requires_activation = 1
        self.user.save()

        response = self.client.post(
            self.link % (self.user.pk, make_password_change_token(self.user))
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "Your link has expired. Please request new one."},
        )

        self.user.requires_activation = 2
        self.user.save()

        response = self.client.post(
            self.link % (self.user.pk, make_password_change_token(self.user))
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "Your link has expired. Please request new one."},
        )

    def test_disabled_user(self):
        """change password api errors for disabled users"""
        self.user.is_active = False
        self.user.save()

        response = self.client.post(
            self.link % (self.user.pk, make_password_change_token(self.user))
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"detail": "Form link is invalid. Please try again."}
        )

    def test_submit_empty(self):
        """change password api errors for empty body"""
        response = self.client.post(
            self.link % (self.user.pk, make_password_change_token(self.user))
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "detail": "This password is too short. It must contain at least 7 characters."
            },
        )
