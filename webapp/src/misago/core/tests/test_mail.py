from django.core import mail
from django.test import TestCase
from django.urls import reverse

from ...cache.versions import get_cache_versions
from ...conf.dynamicsettings import DynamicSettings
from ...conf.test import override_dynamic_settings
from ...users.test import create_test_user
from ..mail import build_mail, mail_user, mail_users


class MailTests(TestCase):
    def test_building_mail_without_context_raises_value_error(self):
        user = create_test_user("User", "user@example.com")
        with self.assertRaises(ValueError):
            build_mail(user, "Misago Test Mail", "misago/emails/base")

    def test_building_mail_without_settings_in_context_raises_value_error(self):
        user = create_test_user("User", "user@example.com")
        with self.assertRaises(ValueError):
            build_mail(
                user, "Misago Test Mail", "misago/emails/base", context={"settings": {}}
            )

    @override_dynamic_settings(forum_address="http://test.com/")
    def test_mail_user(self):
        """mail_user sets message in backend"""
        user = create_test_user("User", "user@example.com")

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
        user_avatar_url = reverse(
            "misago:user-avatar", kwargs={"pk": user.pk, "size": 32}
        )

        self.assertIn(user_avatar_url, html_body)

    def test_mail_users(self):
        """mail_users sets messages in backend"""
        cache_versions = get_cache_versions()
        settings = DynamicSettings(cache_versions)

        test_users = [
            create_test_user("User1", "User1@example.com"),
            create_test_user("Use2r", "User2@example.com"),
            create_test_user("Us3er", "User3@example.com"),
            create_test_user("U4ser", "User4@example.com"),
            create_test_user("5User", "User5@example.com"),
        ]

        mail_users(
            test_users,
            "Misago Test Spam",
            "misago/emails/base",
            context={"settings": settings},
        )

        spams_sent = 0
        for message in mail.outbox:
            if message.subject == "Misago Test Spam":
                spams_sent += 1

        self.assertEqual(spams_sent, len(test_users))
