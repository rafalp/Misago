from django.test import TestCase

from ..models import Ban


class BansManagerTests(TestCase):
    def setUp(self):
        Ban.objects.bulk_create(
            [
                Ban(check_type=Ban.USERNAME, banned_value="user"),
                Ban(check_type=Ban.EMAIL, banned_value="user@example.com"),
                Ban(check_type=Ban.IP, banned_value="127.0.0.1"),
            ]
        )

    def test_get_ban_for_banned_name(self):
        """get_ban finds ban for given username"""
        self.assertIsNotNone(Ban.objects.get_ban(username="User"))
        with self.assertRaises(Ban.DoesNotExist):
            Ban.objects.get_ban(username="OtherUser")

    def test_get_ban_for_banned_email(self):
        """get_ban finds ban for given email"""
        self.assertIsNotNone(Ban.objects.get_ban(email="user@example.com"))
        with self.assertRaises(Ban.DoesNotExist):
            Ban.objects.get_ban(email="otheruser@example.com")

    def test_get_ban_for_banned_ip(self):
        """get_ban finds ban for given ip"""
        self.assertIsNotNone(Ban.objects.get_ban(ip="127.0.0.1"))
        with self.assertRaises(Ban.DoesNotExist):
            Ban.objects.get_ban(ip="42.0.0.1")

    def test_get_ban_for_all_values(self):
        """get_ban finds ban for given values"""
        valid_kwargs = {"username": "User", "ip": "42.51.52.51"}
        self.assertIsNotNone(Ban.objects.get_ban(**valid_kwargs))

        invalid_kwargs = {"username": "OtherUser", "ip": "42.51.52.51"}
        with self.assertRaises(Ban.DoesNotExist):
            Ban.objects.get_ban(**invalid_kwargs)


class BanTests(TestCase):
    def test_check_value_literal(self):
        """ban correctly tests given values"""
        test_ban = Ban(banned_value="user")

        self.assertTrue(test_ban.check_value("User"))
        self.assertFalse(test_ban.check_value("OtherUser"))
        self.assertFalse(test_ban.check_value("UserOther"))

    def test_check_value_starts_with(self):
        """ban correctly tests given values"""
        test_ban = Ban(banned_value="user*")

        self.assertTrue(test_ban.check_value("User"))
        self.assertTrue(test_ban.check_value("UserOther"))
        self.assertFalse(test_ban.check_value("NewUser"))

    def test_check_value_middle_match(self):
        """ban correctly tests given values"""
        test_ban = Ban(banned_value="u*r")

        self.assertTrue(test_ban.check_value("User"))
        self.assertTrue(test_ban.check_value("UserOther"))
        self.assertFalse(test_ban.check_value("NewUser"))
        self.assertFalse(test_ban.check_value("UserNew"))

    def test_check_value_ends_witch(self):
        """ban correctly tests given values"""
        test_ban = Ban(banned_value="*user")

        self.assertTrue(test_ban.check_value("User"))
        self.assertTrue(test_ban.check_value("OtherUser"))
        self.assertFalse(test_ban.check_value("UserOther"))
