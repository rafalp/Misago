from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase


UserModel = get_user_model()


class CreateSuperUserTests(TestCase):
    def test_createsuperuser(self):
        """createsuperuser creates user account in perfect conditions"""
        opts = {
            'username': 'Boberson',
            'email': 'bob@test.com',
            'password': 'Pass.123',
            'verbosity': 0,
        }

        call_command('createsuperuser', **opts)

        user = UserModel.objects.get(username=opts['username'])
        self.assertEqual(user.username, opts['username'])
        self.assertEqual(user.email, opts['email'])
        self.assertTrue(user.check_password(opts['password']))
