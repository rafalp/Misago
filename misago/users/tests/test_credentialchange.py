from django.contrib.auth import get_user_model
from django.test import TestCase

from misago.users import credentialchange


UserModel = get_user_model()


class MockRequest(object):
    def __init__(self, user):
        self.session = {}
        self.user = user


class CredentialChangeTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user('Bob', 'bob@bob.com', 'pass123')

    def test_valid_token_generation(self):
        """credentialchange module allows for store and read of change token"""
        request = MockRequest(self.user)
        token = credentialchange.store_new_credential(request, 'email', 'newbob@test.com')

        email = credentialchange.read_new_credential(request, 'email', token)
        self.assertEqual(email, 'newbob@test.com')

    def test_email_change_invalidated_token(self):
        """token is invalidated by email change"""
        request = MockRequest(self.user)
        token = credentialchange.store_new_credential(request, 'email', 'newbob@test.com')

        self.user.set_email('egebege@test.com')
        self.user.save()

        email = credentialchange.read_new_credential(request, 'email', token)
        self.assertIsNone(email)

    def test_password_change_invalidated_token(self):
        """token is invalidated by password change"""
        request = MockRequest(self.user)
        token = credentialchange.store_new_credential(request, 'email', 'newbob@test.com')

        self.user.set_password('Egebeg!123')
        self.user.save()

        email = credentialchange.read_new_credential(request, 'email', token)
        self.assertIsNone(email)

    def test_invalid_token_is_handled(self):
        """there are no explosions in invalid tokens handling"""
        request = MockRequest(self.user)
        token = credentialchange.store_new_credential(request, 'email', 'newbob@test.com')

        email = credentialchange.read_new_credential(request, 'em4il', token)
        self.assertIsNone(email)
