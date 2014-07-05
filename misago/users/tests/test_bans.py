from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase

from misago.users.bans import get_user_ban, get_request_ip_ban
from misago.users.models import Ban, BAN_IP


class UserBansTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user('Bob',
                                             'bob@boberson.com',
                                             'pass123')

    def test_no_ban(self):
        """user is not caught by ban"""
        self.assertIsNone(get_user_ban(self.user))
        self.assertFalse(self.user.ban_cache.is_banned)

    def test_permanent_ban(self):
        """user is caught by permanent ban"""
        Ban.objects.create(banned_value='bob',
                           user_message='User reason',
                           staff_message='Staff reason')

        user_ban = get_user_ban(self.user)
        self.assertIsNotNone(user_ban)
        self.assertEqual(user_ban.user_message, 'User reason')
        self.assertEqual(user_ban.staff_message, 'Staff reason')
        self.assertTrue(self.user.ban_cache.is_banned)

    def test_temporary_ban(self):
        """user is caught by temporary ban"""
        Ban.objects.create(banned_value='bo*',
                           user_message='User reason',
                           staff_message='Staff reason',
                           valid_until=date.today() + timedelta(days=7))

        user_ban = get_user_ban(self.user)
        self.assertIsNotNone(user_ban)
        self.assertEqual(user_ban.user_message, 'User reason')
        self.assertEqual(user_ban.staff_message, 'Staff reason')
        self.assertTrue(self.user.ban_cache.is_banned)

    def test_expired_ban(self):
        """user is not caught by expired ban"""
        Ban.objects.create(banned_value='bo*',
                           valid_until=date.today() - timedelta(days=7))

        self.assertIsNone(get_user_ban(self.user))
        self.assertFalse(self.user.ban_cache.is_banned)


class FakeRequest(object):
    def __init__(self):
        self._misago_real_ip = '127.0.0.1'
        self.session = {}


class RequestIPBansTests(TestCase):
    def test_no_ban(self):
        """no ban found"""
        ip_ban = get_request_ip_ban(FakeRequest())
        self.assertIsNone(ip_ban)

    def test_permanent_ban(self):
        """ip is caught by permanent ban"""
        Ban.objects.create(test=BAN_IP,
                           banned_value='127.0.0.1',
                           user_message='User reason')

        ip_ban = get_request_ip_ban(FakeRequest())
        self.assertTrue(ip_ban['is_banned'])
        self.assertEqual(ip_ban['ip'], '127.0.0.1')
        self.assertEqual(ip_ban['message'], 'User reason')

    def test_temporary_ban(self):
        """ip is caught by temporary ban"""
        Ban.objects.create(test=BAN_IP,
                           banned_value='127.0.0.1',
                           user_message='User reason',
                           valid_until=date.today() + timedelta(days=7))

        ip_ban = get_request_ip_ban(FakeRequest())
        self.assertTrue(ip_ban['is_banned'])
        self.assertEqual(ip_ban['ip'], '127.0.0.1')
        self.assertEqual(ip_ban['message'], 'User reason')

    def test_expired_ban(self):
        """ip is not caught by expired ban"""
        Ban.objects.create(test=BAN_IP,
                           banned_value='127.0.0.1',
                           user_message='User reason',
                           valid_until=date.today() - timedelta(days=7))

        ip_ban = get_request_ip_ban(FakeRequest())
        self.assertIsNone(ip_ban)
