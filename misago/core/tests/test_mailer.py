from django.contrib.auth import get_user_model
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase


class MisagoFormsTests(TestCase):
    serialized_rollback = True
    urls = 'misago.core.testproject.urls'

    def test_mail_user(self):
        """mail_user sets message in backend"""
        User = get_user_model()
        test_user = User.objects.create_user('Bob', 'bob@bob.com', 'pass123')

        response = self.client.get(reverse('test_mail_user'))
        self.assertEqual(response.status_code, 200)

        for message in mail.outbox:
            if message.subject == 'Misago Test Mail':
                break
        else:
            self.fail("Message was not added to backend.")

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

        response = self.client.get(reverse('test_mail_users'))
        self.assertEqual(response.status_code, 200)

        spams_sent = 0
        for message in mail.outbox:
            if message.subject == 'Misago Test Spam':
                spams_sent += 1

        self.assertEqual(spams_sent, len(test_users))
