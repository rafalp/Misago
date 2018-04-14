from django.contrib.auth import get_user_model
from django.core import mail
from django.test import override_settings
from django.urls import reverse

from misago.conf import settings
from misago.users.models import Ban, Online
from misago.users.testutils import UserTestCase


UserModel = get_user_model()


class UserCreateTests(UserTestCase):
    """tests for new user registration (POST to /api/users/)"""

    def setUp(self):
        super(UserCreateTests, self).setUp()
        self.api_link = '/api/users/'

    def test_empty_request(self):
        """empty request errors with code 400"""
        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'email': ["This field is required."],
            'password': ["This field is required."],
            'username': ["This field is required."],
        })

    def test_invalid_data(self):
        """invalid request data errors with code 400"""
        response = self.client.post(
            self.api_link,
            'false',
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'non_field_errors': ["Invalid data. Expected a dictionary, but got bool."],
        })

    def test_authenticated_request(self):
        """authentiated user request errors with code 403"""
        self.login_user(self.get_authenticated_user())
        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "This action is not available to signed in users.",
        })

    def test_registration_off_request(self):
        """registrations off request errors with code 403"""
        settings.override_setting('account_activation', 'closed')

        response = self.client.post(self.api_link)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': "New users registrations are currently closed.",
        })

    def test_registration_validates_ip_ban(self):
        """api validates ip ban"""
        Ban.objects.create(
            check_type=Ban.IP,
            banned_value='127.*',
            user_message="You can't register account like this.",
        )

        response = self.client.post(
            self.api_link,
            data={
                'username': 'totallyNew',
                'email': 'loremipsum@dolor.met',
                'password': 'LoremP4ssword',
            },
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'detail': {
                'html': '<p>You can&#39;t register account like this.</p>',
                'plain': "You can't register account like this."
            },
            'expires_on': None,
        })

    def test_registration_validates_ip_registration_ban(self):
        """api validates ip registration-only ban"""
        Ban.objects.create(
            check_type=Ban.IP,
            banned_value='127.*',
            user_message="You can't register account like this.",
            registration_only=True,
        )

        response = self.client.post(
            self.api_link,
            data={
                'username': 'totallyNew',
                'email': 'loremipsum@dolor.met',
                'password': 'LoremP4ssword',
            },
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(), {
                'detail': {
                    'html': '<p>You can&#39;t register account like this.</p>',
                    'plain': "You can't register account like this.",
                },
                'expires_on': None,
            }
        )

    def test_registration_validates_username(self):
        """api validates usernames"""
        user = self.get_authenticated_user()

        response = self.client.post(
            self.api_link,
            data={
                'username': user.username,
                'email': 'loremipsum@dolor.met',
                'password': 'LoremP4ssword',
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'username': ["This username is not available."],
        })

    def test_registration_validates_username_ban(self):
        """api validates username ban"""
        Ban.objects.create(
            banned_value='totally*',
            user_message="You can't register account like this.",
        )

        response = self.client.post(
            self.api_link,
            data={
                'username': 'totallyNew',
                'email': 'loremipsum@dolor.met',
                'password': 'LoremP4ssword',
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {
                'username': ["You can't register account like this."],
            }
        )

    def test_registration_validates_username_registration_ban(self):
        """api validates username registration-only ban"""
        Ban.objects.create(
            banned_value='totally*',
            user_message="You can't register account like this.",
            registration_only=True,
        )

        response = self.client.post(
            self.api_link,
            data={
                'username': 'totallyNew',
                'email': 'loremipsum@dolor.met',
                'password': 'LoremP4ssword',
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {
                'username': ["You can't register account like this."],
            }
        )

    def test_registration_validates_email(self):
        """api validates usernames"""
        user = self.get_authenticated_user()

        response = self.client.post(
            self.api_link,
            data={
                'username': 'totallyNew',
                'email': user.email,
                'password': 'LoremP4ssword',
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'email': ["This e-mail address is not available."],
        })

    def test_registration_validates_email_ban(self):
        """api validates email ban"""
        Ban.objects.create(
            check_type=Ban.EMAIL,
            banned_value='lorem*',
            user_message="You can't register account like this.",
        )

        response = self.client.post(
            self.api_link,
            data={
                'username': 'totallyNew',
                'email': 'loremipsum@dolor.met',
                'password': 'LoremP4ssword',
            },
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'email': ["You can't register account like this."],
        })

    def test_registration_validates_email_registration_ban(self):
        """api validates email registration-only ban"""
        Ban.objects.create(
            check_type=Ban.EMAIL,
            banned_value='lorem*',
            user_message="You can't register account like this.",
            registration_only=True,
        )

        response = self.client.post(
            self.api_link,
            data={
                'username': 'totallyNew',
                'email': 'loremipsum@dolor.met',
                'password': 'LoremP4ssword',
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'email': ["You can't register account like this."],
        })

    def test_registration_validates_password(self):
        """api uses django's validate_password to validate registrations"""
        response = self.client.post(
            self.api_link,
            data={
                'username': 'Bob',
                'email': 'l.o.r.e.m.i.p.s.u.m@gmail.com',
                'password': '123',
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'password': [
                "This password is too short. It must contain at least 7 characters.",
                "This password is entirely numeric.",
            ],
            'email': ["This email is not allowed."],
        })

    def test_registration_validates_password_similiarity(self):
        """api uses validate_password to validate registrations"""
        response = self.client.post(
            self.api_link,
            data={
                'username': 'BobBoberson',
                'email': 'l.o.r.e.m.i.p.s.u.m@gmail.com',
                'password': 'BobBoberson',
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'password': ["The password is too similar to the username."],
            'email': ["This email is not allowed."],
        })

    @override_settings(captcha_type='qa', qa_question='Test', qa_answers='Lorem\nIpsum')
    def test_registration_validates_captcha(self):
        """api validates captcha"""
        response = self.client.post(
            self.api_link,
            data={
                'username': 'totallyNew',
                'email': 'loremipsum@dolor.met',
                'password': 'LoremP4ssword',
                'captcha': 'dolor'
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {
                'captcha': ['Entered answer is incorrect.'],
            }
        )

        # valid captcha
        response = self.client.post(
            self.api_link,
            data={
                'username': 'totallyNew',
                'email': 'loremipsum@dolor.met',
                'password': 'LoremP4ssword',
                'captcha': 'ipSUM'
            },
        )

        self.assertEqual(response.status_code, 200)

    def test_registration_calls_validate_new_registration(self):
        """api uses validate_new_registration to validate registrations"""
        response = self.client.post(
            self.api_link,
            data={
                'username': 'Bob',
                'email': 'l.o.r.e.m.i.p.s.u.m@gmail.com',
                'password': 'pass1234',
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'email': ["This email is not allowed."]
        })

    def test_registration_creates_active_user(self):
        """api creates active and signed in user on POST"""
        settings.override_setting('account_activation', 'none')

        response = self.client.post(
            self.api_link,
            data={
                'username': 'Bob',
                'email': 'bob@bob.com',
                'password': 'pass123',
            },
        )

        self.assertEqual(response.json(), {
            'activation': None,
            'username': 'Bob',
            'email': 'bob@bob.com',
        })

        UserModel.objects.get_by_username('Bob')

        test_user = UserModel.objects.get_by_email('bob@bob.com')
        self.assertEqual(Online.objects.filter(user=test_user).count(), 1)

        self.assertTrue(test_user.check_password('pass123'))

        response = self.client.get(reverse('misago:index'))
        self.assertContains(response, 'Bob')

        self.assertIn('Welcome', mail.outbox[0].subject)

    def test_registration_creates_inactive_user(self):
        """api creates inactive user on POST"""
        settings.override_setting('account_activation', 'user')

        response = self.client.post(
            self.api_link,
            data={
                'username': 'Bob',
                'email': 'bob@bob.com',
                'password': 'pass123',
            },
        )

        self.assertEqual(response.json(), {
            'activation': 'user',
            'username': 'Bob',
            'email': 'bob@bob.com',
        })

        UserModel.objects.get_by_username('Bob')
        UserModel.objects.get_by_email('bob@bob.com')

        self.assertIn('Welcome', mail.outbox[0].subject)

    def test_registration_creates_admin_activated_user(self):
        """api creates admin activated user on POST"""
        settings.override_setting('account_activation', 'admin')

        response = self.client.post(
            self.api_link,
            data={
                'username': 'Bob',
                'email': 'bob@bob.com',
                'password': 'pass123',
            },
        )

        self.assertEqual(response.json(), {
            'activation': 'admin',
            'username': 'Bob',
            'email': 'bob@bob.com',
        })

        UserModel.objects.get_by_username('Bob')
        UserModel.objects.get_by_email('bob@bob.com')

        self.assertIn('Welcome', mail.outbox[0].subject)

    def test_registration_creates_user_with_whitespace_password(self):
        """api creates user with spaces around password"""
        settings.override_setting('account_activation', 'none')

        response = self.client.post(
            self.api_link,
            data={
                'username': 'Bob',
                'email': 'bob@bob.com',
                'password': ' pass123 ',
            },
        )

        self.assertEqual(response.json(), {
            'activation': None,
            'username': 'Bob',
            'email': 'bob@bob.com',
        })

        UserModel.objects.get_by_username('Bob')

        test_user = UserModel.objects.get_by_email('bob@bob.com')
        self.assertEqual(Online.objects.filter(user=test_user).count(), 1)

        self.assertTrue(test_user.check_password(' pass123 '))

        response = self.client.get(reverse('misago:index'))
        self.assertContains(response, 'Bob')

        self.assertIn('Welcome', mail.outbox[0].subject)
