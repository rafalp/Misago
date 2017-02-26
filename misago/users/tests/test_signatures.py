from django.contrib.auth import get_user_model
from django.test import TestCase

from misago.users import signatures


UserModel = get_user_model()


class MockRequest(object):
    scheme = 'http'

    def get_host(self):
        return '127.0.0.1:8000'


class SignaturesTests(TestCase):
    def test_signature_change(self):
        """signature module allows for signature change"""
        test_user = UserModel.objects.create_user('Bob', 'bob@bob.com', 'pass123')

        signatures.set_user_signature(MockRequest(), test_user, '')

        self.assertEqual(test_user.signature, '')
        self.assertEqual(test_user.signature_parsed, '')
        self.assertEqual(test_user.signature_checksum, '')

        signatures.set_user_signature(MockRequest(), test_user, 'Hello, world!')

        self.assertEqual(test_user.signature, 'Hello, world!')
        self.assertEqual(test_user.signature_parsed, '<p>Hello, world!</p>')
        self.assertTrue(signatures.is_user_signature_valid(test_user))

        test_user.signature_parsed = '<p>Injected evil HTML!</p>'
        self.assertFalse(signatures.is_user_signature_valid(test_user))
