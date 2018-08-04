from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from misago.core.mail import mail_user, mail_users


UserModel = get_user_model()


class MailTests(TestCase):
    def test_mail_user(self):
        """mail_user sets message in backend"""
        user = UserModel.objects.create_user('Bob', 'bob@bob.com', 'pass123')

        mail_user(user, "Misago Test Mail", "misago/emails/base")

        self.assertEqual(mail.outbox[0].subject, "Misago Test Mail")

        # assert that url to user's avatar is valid
        html_body = mail.outbox[0].alternatives[0][0]
        user_avatar_url = reverse('misago:user-avatar', kwargs={'pk': user.pk, 'size': 32})

        self.assertIn(user_avatar_url, html_body)

    def test_mail_users(self):
        """mail_users sets messages in backend"""
        test_users = [
            UserModel.objects.create_user('Alpha', 'alpha@test.com', 'pass123'),
            UserModel.objects.create_user('Beta', 'beta@test.com', 'pass123'),
            UserModel.objects.create_user('Niner', 'niner@test.com', 'pass123'),
            UserModel.objects.create_user('Foxtrot', 'foxtrot@test.com', 'pass123'),
            UserModel.objects.create_user('Uniform', 'uniform@test.com', 'pass123'),
        ]

        mail_users(test_users, "Misago Test Spam", "misago/emails/base")

        spams_sent = 0
        for message in mail.outbox:
            if message.subject == 'Misago Test Spam':
                spams_sent += 1

        self.assertEqual(spams_sent, len(test_users))
