#-*- coding: utf-8 -*-
from django.test import TestCase

from misago.users.models import Ban


class BansManagerTests(TestCase):
    def setUp(self):
        Ban.objects.bulk_create([
            Ban(check_type=Ban.USERNAME, banned_value='bob'),
            Ban(check_type=Ban.EMAIL, banned_value='bob@test.com'),
            Ban(check_type=Ban.IP, banned_value='127.0.0.1'),
        ])

    def test_get_ban_for_banned_name(self):
        """get_ban finds ban for given username"""
        self.assertIsNotNone(Ban.objects.get_ban(username='Bob'))
        with self.assertRaises(Ban.DoesNotExist):
            Ban.objects.get_ban(username='Jeb')

    def test_get_ban_for_banned_email(self):
        """get_ban finds ban for given email"""
        self.assertIsNotNone(Ban.objects.get_ban(email='bob@test.com'))
        with self.assertRaises(Ban.DoesNotExist):
            Ban.objects.get_ban(email='jeb@test.com')

    def test_get_ban_for_banned_ip(self):
        """get_ban finds ban for given ip"""
        self.assertIsNotNone(Ban.objects.get_ban(ip='127.0.0.1'))
        with self.assertRaises(Ban.DoesNotExist):
            Ban.objects.get_ban(ip='42.0.0.1')

    def test_get_ban_for_all_bans(self):
        """get_ban finds ban for given values"""
        valid_kwargs = {'username': 'bob', 'ip': '42.51.52.51'}
        self.assertIsNotNone(Ban.objects.get_ban(**valid_kwargs))

        invalid_kwargs = {'username': 'bsob', 'ip': '42.51.52.51'}
        with self.assertRaises(Ban.DoesNotExist):
            Ban.objects.get_ban(**invalid_kwargs)


class BanTests(TestCase):
    def test_check_value_literal(self):
        """ban correctly tests given values"""
        test_ban = Ban(banned_value='bob')

        self.assertTrue(test_ban.check_value('bob'))
        self.assertFalse(test_ban.check_value('bobby'))

    def test_check_value_starts_with(self):
        """ban correctly tests given values"""
        test_ban = Ban(banned_value='bob*')

        self.assertTrue(test_ban.check_value('bob'))
        self.assertTrue(test_ban.check_value('bobby'))

    def test_check_value_middle_match(self):
        """ban correctly tests given values"""
        test_ban = Ban(banned_value='b*b')

        self.assertTrue(test_ban.check_value('bob'))
        self.assertFalse(test_ban.check_value('bobby'))

    def test_check_value_ends_witch(self):
        """ban correctly tests given values"""
        test_ban = Ban(banned_value='*bob')

        self.assertTrue(test_ban.check_value('lebob'))
        self.assertFalse(test_ban.check_value('bobby'))
