from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(ROOT_URLCONF='misago.core.testproject.urls')
class MisagoMailerTests(TestCase):
    def test_mail_user(self):
        """mail_user sets message in backend"""
        User = get_user_model()
        user = User.objects.create_user('Bob', 'bob@bob.com', 'pass123')

        response = self.client.get(reverse('test-mail-user'))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(mail.outbox[0].subject, "Misago Test Mail")

        # assert that url to user's avatar is valid
        html_body = mail.outbox[0].alternatives[0][0]
        user_avatar_url = 'http://testserver%s' % user.avatars[0]['url']
        self.assertIn(user_avatar_url, html_body)

    def test_mail_users(self):
        """mail_users sets messages in backend"""
        User = get_user_model()
        test_users = (
            User.objects.create_user('Alpha', 'alpha@test.com', 'pass123'),
            User.objects.create_user('Beta', 'beta@test.com', 'pass123'),
            User.objects.create_user('Niner', 'niner@test.com', 'pass123'),
            User.objects.create_user('Foxtrot', 'foxtrot@test.com', 'pass123'),
            User.objects.create_user('Uniform', 'uniform@test.com', 'pass123'),
        )

        response = self.client.get(reverse('test-mail-users'))
        self.assertEqual(response.status_code, 200)

        spams_sent = 0
        for message in mail.outbox:
            if message.subject == 'Misago Test Spam':
                spams_sent += 1

        self.assertEqual(spams_sent, len(test_users))
