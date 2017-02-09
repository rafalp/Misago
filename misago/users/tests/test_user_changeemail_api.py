from django.contrib.auth import get_user_model
from django.core import mail

from misago.users.testutils import AuthenticatedUserTestCase


UserModel = get_user_model()


class UserChangeEmailTests(AuthenticatedUserTestCase):
    """
    tests for user change email RPC (/api/users/1/change-email/)
    """
    def setUp(self):
        super(UserChangeEmailTests, self).setUp()
        self.link = '/api/users/%s/change-email/' % self.user.pk

    def test_unsupported_methods(self):
        """api isn't supporting GET"""
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 405)

    def test_change_email(self):
        """api allows users to change their e-mail addresses"""
        response = self.client.post(self.link, data={
            'new_email': 'new@email.com',
            'password': self.USER_PASSWORD
        })
        self.assertEqual(response.status_code, 200)

        self.assertIn('Confirm e-mail change', mail.outbox[0].subject)
        for line in [l.strip() for l in mail.outbox[0].body.splitlines()]:
            if line.startswith('http://'):
                token = line.rstrip('/').split('/')[-1]
                break
        else:
            self.fail("E-mail sent didn't contain confirmation url")

    def test_invalid_password(self):
        """api errors correctly for invalid password"""
        response = self.client.post(self.link, data={
            'new_email': 'new@email.com',
            'password': 'Lor3mIpsum'
        })
        self.assertContains(response, 'password is invalid', status_code=400)

    def test_invalid_input(self):
        """api errors correctly for invalid input"""
        response = self.client.post(self.link, data={
            'new_email': '',
            'password': self.USER_PASSWORD
        })
        self.assertContains(response, 'new_email":["This field is required', status_code=400)

        response = self.client.post(self.link, data={
            'new_email': 'newmail',
            'password': self.USER_PASSWORD
        })
        self.assertContains(response, 'valid email address', status_code=400)

    def test_email_taken(self):
        """api validates email usage"""
        UserModel.objects.create_user('BobBoberson', 'new@email.com', 'Pass.123')

        response = self.client.post(self.link, data={
            'new_email': 'new@email.com',
            'password': self.USER_PASSWORD
        })
        self.assertContains(response, 'not available', status_code=400)
