from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from misago.cache.versions import get_cache_versions
from misago.conf.dynamicsettings import DynamicSettings

from misago.core.mail import build_mail, mail_user, mail_users


UserModel = get_user_model()


class MailTests(TestCase):
    def test_building_mail_without_context_raises_value_error(self):
        user = UserModel.objects.create_user('Bob', 'bob@bob.com', 'pass123')
        with self.assertRaises(ValueError):
            build_mail(user, "Misago Test Mail", "misago/emails/base")

    def test_building_mail_without_settings_in_context_raises_value_error(self):
        user = UserModel.objects.create_user('Bob', 'bob@bob.com', 'pass123')
        with self.assertRaises(ValueError):
            build_mail(user, "Misago Test Mail", "misago/emails/base", context={"settings": {}})

    def test_mail_user(self):
        """mail_user sets message in backend"""
        user = UserModel.objects.create_user('Bob', 'bob@bob.com', 'pass123')

        cache_versions = get_cache_versions()
        settings = DynamicSettings(cache_versions)

        mail_user(
            user,
            "Misago Test Mail",
            "misago/emails/base",
            context={"settings": settings},
        )

        self.assertEqual(mail.outbox[0].subject, "Misago Test Mail")

        # assert that url to user's avatar is valid
        html_body = mail.outbox[0].alternatives[0][0]
        user_avatar_url = reverse('misago:user-avatar', kwargs={'pk': user.pk, 'size': 32})

        self.assertIn(user_avatar_url, html_body)

    def test_mail_users(self):
        """mail_users sets messages in backend"""
        cache_versions = get_cache_versions()
        settings = DynamicSettings(cache_versions)

        test_users = [
            UserModel.objects.create_user('Alpha', 'alpha@test.com', 'pass123'),
            UserModel.objects.create_user('Beta', 'beta@test.com', 'pass123'),
            UserModel.objects.create_user('Niner', 'niner@test.com', 'pass123'),
            UserModel.objects.create_user('Foxtrot', 'foxtrot@test.com', 'pass123'),
            UserModel.objects.create_user('Uniform', 'uniform@test.com', 'pass123'),
        ]

        mail_users(
            test_users,
            "Misago Test Spam",
            "misago/emails/base",
            context={"settings": settings},
        )

        spams_sent = 0
        for message in mail.outbox:
            if message.subject == 'Misago Test Spam':
                spams_sent += 1

        self.assertEqual(spams_sent, len(test_users))
