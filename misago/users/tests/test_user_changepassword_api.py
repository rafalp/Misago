from django.contrib.auth import get_user_model
from django.core import mail
from misago.users.testutils import AuthenticatedUserTestCase


class UserChangePasswordTests(AuthenticatedUserTestCase):
    """
    tests for user change password RPC (/api/users/1/change-password/)
    """
    def setUp(self):
        super(UserChangePasswordTests, self).setUp()
        self.link = '/api/users/%s/change-password/' % self.user.pk

    def test_unsupported_methods(self):
        """api isn't supporting GET"""
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 405)

    def test_change_email(self):
        """api allows users to change their passwords"""
        response = self.client.post(self.link, data={
            'new_password': 'N3wP@55w0rd',
            'password': self.USER_PASSWORD
        })
        self.assertEqual(response.status_code, 200)

        self.assertIn('Confirm password change', mail.outbox[0].subject)
        for line in [l.strip() for l in mail.outbox[0].body.splitlines()]:
            if line.startswith('http://'):
                token = line.rstrip('/').split('/')[-1]
                break
        else:
            self.fail("E-mail sent didn't contain confirmation url")

        response = self.client.post(self.link, data={'token': token})
        self.assertEqual(response.status_code, 200)

        self.reload_user()
        self.assertTrue(self.user.check_password('N3wP@55w0rd'))

    def test_invalid_password(self):
        """api errors correctly for invalid password"""
        response = self.client.post(self.link, data={
            'new_password': 'N3wP@55w0rd',
            'password': 'Lor3mIpsum'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('password is invalid', response.content)

    def test_invalid_input(self):
        """api errors correctly for invalid input"""
        response = self.client.post(self.link, data={
            'new_password': '',
            'password': self.USER_PASSWORD
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('enter new password', response.content)

        response = self.client.post(self.link, data={
            'new_password': 'n',
            'password': self.USER_PASSWORD
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('password must be', response.content)

    def test_invalid_token(self):
        """api handles invalid token"""
        response = self.client.post(self.link, data={
            'new_password': 'N3wP@55w0rd',
            'password': self.USER_PASSWORD
        })
        self.assertEqual(response.status_code, 200)

        response = self.client.post(self.link, data={'token': 'invalid-token'})
        self.assertEqual(response.status_code, 400)

        self.reload_user()
        self.assertFalse(self.user.check_password('N3wP@55w0rd'))

    def test_expired_token(self):
        """api handles invalid token"""
        response = self.client.post(self.link, data={
            'new_password': 'N3wP@55w0rd',
            'password': self.USER_PASSWORD
        })
        self.assertEqual(response.status_code, 200)

        for line in [l.strip() for l in mail.outbox[0].body.splitlines()]:
            if line.startswith('http://'):
                token = line.rstrip('/').split('/')[-1]
                break
        else:
            self.fail("E-mail sent didn't contain confirmation url")

        self.user.set_email('new@email.com')
        self.user.save()

        response = self.client.post(self.link, data={'token': 'invalid-token'})
        self.assertEqual(response.status_code, 400)

        self.reload_user()
        self.assertFalse(self.user.check_password('N3wP@55w0rd'))
