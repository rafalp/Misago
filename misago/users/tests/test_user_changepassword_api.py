from django.core import mail
from django.urls import reverse

from misago.users.testutils import AuthenticatedUserTestCase


class UserChangePasswordTests(AuthenticatedUserTestCase):
    """tests for user change password RPC (/api/users/1/change-password/)"""

    def setUp(self):
        super(UserChangePasswordTests, self).setUp()
        self.link = '/api/users/%s/change-password/' % self.user.pk

    def test_unsupported_methods(self):
        """api isn't supporting GET"""
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, 405)

    def test_empty_input(self):
        """api errors correctly for empty input"""
        response = self.client.post(self.link, data={})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {
                'new_password': ["This field is required."],
                'password': ["This field is required."],
            }
        )

    def test_invalid_password(self):
        """api errors correctly for invalid password"""
        response = self.client.post(
            self.link,
            data={
                'new_password': 'N3wP@55w0rd',
                'password': 'Lor3mIpsum',
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'password': ["Entered password is invalid."],
        })

    def test_blank_input(self):
        """api errors correctly for blank input"""
        response = self.client.post(
            self.link,
            data={
                'new_password': '',
                'password': self.USER_PASSWORD,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'new_password': ["This field may not be blank."],
        })

    def test_short_new_pasword(self):
        """api errors correctly for short new password"""
        response = self.client.post(
            self.link,
            data={
                'new_password': 'n',
                'password': self.USER_PASSWORD,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {
                'new_password':
                    ["This password is too short. It must contain at least 7 characters."],
            }
        )

    def test_change_password(self):
        """api allows users to change their passwords"""
        new_password = 'N3wP@55w0rd'

        response = self.client.post(
            self.link,
            data={
                'new_password': new_password,
                'password': self.USER_PASSWORD,
            },
        )
        self.assertEqual(response.status_code, 200)

        self.assertIn('Confirm password change', mail.outbox[0].subject)
        for line in [l.strip() for l in mail.outbox[0].body.splitlines()]:
            if line.startswith('http://'):
                token = line.rstrip('/').split('/')[-1]
                break
        else:
            self.fail("E-mail sent didn't contain confirmation url")

        response = self.client.get(
            reverse('misago:options-confirm-password-change', kwargs={
                'token': token,
            })
        )

        self.assertEqual(response.status_code, 200)

        self.reload_user()
        self.assertTrue(self.user.check_password(new_password))

    def test_change_password_with_whitespaces(self):
        """api handles users with whitespaces around their passwords"""
        old_password = ' old password '
        new_password = ' N3wP@55w0rd '

        self.user.set_password(old_password)
        self.user.save()

        self.login_user(self.user)

        response = self.client.post(
            self.link,
            data={
                'new_password': new_password,
                'password': old_password,
            },
        )
        self.assertEqual(response.status_code, 200)

        self.assertIn('Confirm password change', mail.outbox[0].subject)
        for line in [l.strip() for l in mail.outbox[0].body.splitlines()]:
            if line.startswith('http://'):
                token = line.rstrip('/').split('/')[-1]
                break
        else:
            self.fail("E-mail sent didn't contain confirmation url")

        response = self.client.get(
            reverse('misago:options-confirm-password-change', kwargs={
                'token': token,
            })
        )

        self.assertEqual(response.status_code, 200)

        self.reload_user()
        self.assertTrue(self.user.check_password(new_password))
