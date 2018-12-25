from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from ...conftest import get_cache_versions
from ..bans import (
    ban_ip,
    ban_user,
    get_email_ban,
    get_ip_ban,
    get_request_ip_ban,
    get_user_ban,
    get_username_ban,
)
from ..models import Ban
from ..test import create_test_user

cache_versions = get_cache_versions()


class GetBanTests(TestCase):
    def test_get_username_ban(self):
        """get_username_ban returns valid ban"""
        nonexistent_ban = get_username_ban("nonexistent")
        self.assertIsNone(nonexistent_ban)

        Ban.objects.create(
            banned_value="expired", expires_on=timezone.now() - timedelta(days=7)
        )

        expired_ban = get_username_ban("expired")
        self.assertIsNone(expired_ban)

        Ban.objects.create(banned_value="wrongtype", check_type=Ban.EMAIL)

        wrong_type_ban = get_username_ban("wrongtype")
        self.assertIsNone(wrong_type_ban)

        valid_ban = Ban.objects.create(
            banned_value="admi*", expires_on=timezone.now() + timedelta(days=7)
        )
        self.assertEqual(get_username_ban("admiral").pk, valid_ban.pk)

        registration_ban = Ban.objects.create(
            banned_value="mod*",
            expires_on=timezone.now() + timedelta(days=7),
            registration_only=True,
        )
        self.assertIsNone(get_username_ban("moderator"))
        self.assertEqual(get_username_ban("moderator", True).pk, registration_ban.pk)

    def test_get_email_ban(self):
        """get_email_ban returns valid ban"""
        nonexistent_ban = get_email_ban("non@existent.com")
        self.assertIsNone(nonexistent_ban)

        Ban.objects.create(
            banned_value="ex@pired.com",
            check_type=Ban.EMAIL,
            expires_on=timezone.now() - timedelta(days=7),
        )

        expired_ban = get_email_ban("ex@pired.com")
        self.assertIsNone(expired_ban)

        Ban.objects.create(banned_value="wrong@type.com", check_type=Ban.IP)

        wrong_type_ban = get_email_ban("wrong@type.com")
        self.assertIsNone(wrong_type_ban)

        valid_ban = Ban.objects.create(
            banned_value="*.ru",
            check_type=Ban.EMAIL,
            expires_on=timezone.now() + timedelta(days=7),
        )
        self.assertEqual(get_email_ban("banned@mail.ru").pk, valid_ban.pk)

        registration_ban = Ban.objects.create(
            banned_value="*.ua",
            check_type=Ban.EMAIL,
            expires_on=timezone.now() + timedelta(days=7),
            registration_only=True,
        )
        self.assertIsNone(get_email_ban("banned@mail.ua"))
        self.assertEqual(get_email_ban("banned@mail.ua", True).pk, registration_ban.pk)

    def test_get_ip_ban(self):
        """get_ip_ban returns valid ban"""
        nonexistent_ban = get_ip_ban("123.0.0.1")
        self.assertIsNone(nonexistent_ban)

        Ban.objects.create(
            banned_value="124.0.0.1",
            check_type=Ban.IP,
            expires_on=timezone.now() - timedelta(days=7),
        )

        expired_ban = get_ip_ban("124.0.0.1")
        self.assertIsNone(expired_ban)

        Ban.objects.create(banned_value="wrongtype", check_type=Ban.EMAIL)

        wrong_type_ban = get_ip_ban("wrongtype")
        self.assertIsNone(wrong_type_ban)

        valid_ban = Ban.objects.create(
            banned_value="125.0.0.*",
            check_type=Ban.IP,
            expires_on=timezone.now() + timedelta(days=7),
        )
        self.assertEqual(get_ip_ban("125.0.0.1").pk, valid_ban.pk)

        registration_ban = Ban.objects.create(
            banned_value="188.*",
            check_type=Ban.IP,
            expires_on=timezone.now() + timedelta(days=7),
            registration_only=True,
        )
        self.assertIsNone(get_ip_ban("188.12.12.41"))
        self.assertEqual(get_ip_ban("188.12.12.41", True).pk, registration_ban.pk)


class UserBansTests(TestCase):
    def setUp(self):
        self.user = create_test_user("User", "user@example.com")

    def test_no_ban(self):
        """user is not caught by ban"""
        self.assertIsNone(get_user_ban(self.user, cache_versions))
        self.assertFalse(self.user.ban_cache.is_banned)

    def test_permanent_ban(self):
        """user is caught by permanent ban"""
        Ban.objects.create(
            banned_value="User",
            user_message="User reason",
            staff_message="Staff reason",
        )

        user_ban = get_user_ban(self.user, cache_versions)
        self.assertIsNotNone(user_ban)
        self.assertEqual(user_ban.user_message, "User reason")
        self.assertEqual(user_ban.staff_message, "Staff reason")
        self.assertTrue(self.user.ban_cache.is_banned)

    def test_temporary_ban(self):
        """user is caught by temporary ban"""
        Ban.objects.create(
            banned_value="us*",
            user_message="User reason",
            staff_message="Staff reason",
            expires_on=timezone.now() + timedelta(days=7),
        )

        user_ban = get_user_ban(self.user, cache_versions)
        self.assertIsNotNone(user_ban)
        self.assertEqual(user_ban.user_message, "User reason")
        self.assertEqual(user_ban.staff_message, "Staff reason")
        self.assertTrue(self.user.ban_cache.is_banned)

    def test_expired_ban(self):
        """user is not caught by expired ban"""
        Ban.objects.create(
            banned_value="us*", expires_on=timezone.now() - timedelta(days=7)
        )

        self.assertIsNone(get_user_ban(self.user, cache_versions))
        self.assertFalse(self.user.ban_cache.is_banned)

    def test_expired_non_flagged_ban(self):
        """user is not caught by expired but checked ban"""
        Ban.objects.create(
            banned_value="us*", expires_on=timezone.now() - timedelta(days=7)
        )
        Ban.objects.update(is_checked=True)

        self.assertIsNone(get_user_ban(self.user, cache_versions))
        self.assertFalse(self.user.ban_cache.is_banned)


class MockRequest:
    def __init__(self):
        self.user_ip = "127.0.0.1"
        self.session = {}
        self.cache_versions = cache_versions


class RequestIPBansTests(TestCase):
    def test_no_ban(self):
        """no ban found"""
        ip_ban = get_request_ip_ban(MockRequest())
        self.assertIsNone(ip_ban)

    def test_permanent_ban(self):
        """ip is caught by permanent ban"""
        Ban.objects.create(
            check_type=Ban.IP, banned_value="127.0.0.1", user_message="User reason"
        )

        ip_ban = get_request_ip_ban(MockRequest())
        self.assertTrue(ip_ban["is_banned"])
        self.assertEqual(ip_ban["ip"], "127.0.0.1")
        self.assertEqual(ip_ban["message"], "User reason")

        # repeated call uses cache
        get_request_ip_ban(MockRequest())

    def test_temporary_ban(self):
        """ip is caught by temporary ban"""
        Ban.objects.create(
            check_type=Ban.IP,
            banned_value="127.0.0.1",
            user_message="User reason",
            expires_on=timezone.now() + timedelta(days=7),
        )

        ip_ban = get_request_ip_ban(MockRequest())
        self.assertTrue(ip_ban["is_banned"])
        self.assertEqual(ip_ban["ip"], "127.0.0.1")
        self.assertEqual(ip_ban["message"], "User reason")

        # repeated call uses cache
        get_request_ip_ban(MockRequest())

    def test_expired_ban(self):
        """ip is not caught by expired ban"""
        Ban.objects.create(
            check_type=Ban.IP,
            banned_value="127.0.0.1",
            user_message="User reason",
            expires_on=timezone.now() - timedelta(days=7),
        )

        ip_ban = get_request_ip_ban(MockRequest())
        self.assertIsNone(ip_ban)

        # repeated call uses cache
        get_request_ip_ban(MockRequest())


class BanUserTests(TestCase):
    def test_ban_user(self):
        """ban_user utility bans user"""
        user = create_test_user("User", "user@example.com")

        ban = ban_user(user, "User reason", "Staff reason")
        self.assertEqual(ban.user_message, "User reason")
        self.assertEqual(ban.staff_message, "Staff reason")

        db_ban = get_user_ban(user, cache_versions)
        self.assertEqual(ban.pk, db_ban.ban_id)


class BanIpTests(TestCase):
    def test_ban_ip(self):
        """ban_ip utility bans IP address"""
        ban = ban_ip("127.0.0.1", "User reason", "Staff reason")
        self.assertEqual(ban.user_message, "User reason")
        self.assertEqual(ban.staff_message, "Staff reason")

        db_ban = get_ip_ban("127.0.0.1")
        self.assertEqual(ban.pk, db_ban.pk)
