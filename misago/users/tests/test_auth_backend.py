from django.contrib.auth import get_user_model
from django.test import TestCase

from misago.users.authbackends import MisagoBackend


UserModel = get_user_model()

backend = MisagoBackend()


class MisagoBackendTests(TestCase):
    def setUp(self):
        self.password = 'Pass.123'
        self.user = UserModel.objects.create_user('BobBoberson', 'bob@test.com', self.password)

    def test_authenticate_username(self):
        """auth authenticates with username"""
        user = backend.authenticate(
            None,
            username=self.user.username,
            password=self.password,
        )

        self.assertEqual(user, self.user)

    def test_authenticate_email(self):
        """auth authenticates with email instead of username"""
        user = backend.authenticate(
            None,
            username=self.user.email,
            password=self.password,
        )

        self.assertEqual(user, self.user)

    def test_authenticate_invalid_credential(self):
        """auth handles invalid credentials"""
        user = backend.authenticate(
            None,
            username='InvalidCredential',
            password=self.password,
        )

        self.assertIsNone(user)

    def test_authenticate_invalid_password(self):
        """auth validates password"""
        user = backend.authenticate(
            None,
            username=self.user.email,
            password='Invalid',
        )

        self.assertIsNone(user)

    def test_authenticate_disabled_user(self):
        """auth validates disabled state"""
        self.user.is_active = False
        self.user.save()

        user = backend.authenticate(
            None,
            username=self.user.email,
            password=self.password,
        )

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
