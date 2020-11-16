from django.test import TestCase

from ..authbackends import MisagoBackend
from ..test import create_test_user

backend = MisagoBackend()


class MisagoBackendTests(TestCase):
    def setUp(self):
        self.password = "password"
        self.user = create_test_user("User", "user@example.com", self.password)

    def test_authenticate_username(self):
        """auth authenticates with username"""
        user = backend.authenticate(
            None, username=self.user.username, password=self.password
        )

        self.assertEqual(user, self.user)

    def test_authenticate_email(self):
        """auth authenticates with email instead of username"""
        user = backend.authenticate(
            None, username=self.user.email, password=self.password
        )

        self.assertEqual(user, self.user)

    def test_authenticate_username_and_email(self):
        """auth authenticates with email and skips username"""
        user = backend.authenticate(
            None,
            username=self.user.username,
            password=self.password,
            email=self.user.email,
        )

        self.assertEqual(user, self.user)

    def test_authenticate_wrong_username_and_email(self):
        """auth authenticates with email and invalid username"""
        user = backend.authenticate(
            None,
            username="skipped-username",
            password=self.password,
            email=self.user.email,
        )

        self.assertEqual(user, self.user)

    def test_authenticate_invalid_credential(self):
        """auth handles invalid credentials"""
        user = backend.authenticate(
            None, username="InvalidCredential", password=self.password
        )

        self.assertIsNone(user)

    def test_authenticate_invalid_password(self):
        """auth validates password"""
        user = backend.authenticate(None, username=self.user.email, password="Invalid")

        self.assertIsNone(user)

    def test_authenticate_disabled_user(self):
        """auth validates disabled state"""
        self.user.is_active = False
        self.user.save()

        user = backend.authenticate(
            None, username=self.user.email, password=self.password
        )

        self.assertIsNone(user)

    def test_authenticate_no_data(self):
        """auth has no errors if no recognised credentials are provided"""
        self.user.is_active = False
        self.user.save()

        user = backend.authenticate(None)

        self.assertIsNone(user)

    def test_get_user_valid_pk(self):
        """auth backend returns active user for pk given"""
        self.assertEqual(backend.get_user(self.user.pk), self.user)

    def test_get_user_invalid_pk(self):
        """auth backend returns none for invalid pk"""
        self.assertIsNone(backend.get_user(self.user.pk + 1))

    def test_get_user_disabled(self):
        """auth backend returns none for disabled user"""
        self.user.is_active = False
        self.user.save()

        self.assertIsNone(backend.get_user(self.user.pk))
