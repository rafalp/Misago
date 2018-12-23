from datetime import timedelta
from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from ...cache.versions import get_cache_versions
from ...users import bans
from ..management.commands import invalidatebans
from ..models import Ban, BanCache
from ..test import create_test_user


class InvalidateBansTests(TestCase):
    def test_expired_bans_handling(self):
        """expired bans are flagged as such"""
        # create 5 bans then update their valid date to past one
        for _ in range(5):
            Ban.objects.create(banned_value="abcd")
        expired_date = timezone.now() - timedelta(days=10)
        Ban.objects.all().update(expires_on=expired_date, is_checked=True)

        self.assertEqual(Ban.objects.filter(is_checked=True).count(), 5)

        command = invalidatebans.Command()

        out = StringIO()
        call_command(command, stdout=out)
        command_output = out.getvalue().splitlines()[0].strip()

        self.assertEqual(command_output, "Bans invalidated: 5")

        self.assertEqual(Ban.objects.filter(is_checked=True).count(), 0)

    def test_bans_caches_updates(self):
        """ban caches are updated"""
        user = create_test_user("User", "user@example.com")

        # ban user
        Ban.objects.create(banned_value="user")
        user_ban = bans.get_user_ban(user, get_cache_versions())

        self.assertIsNotNone(user_ban)
        self.assertEqual(Ban.objects.filter(is_checked=True).count(), 1)

        # first call didn't touch ban
        command = invalidatebans.Command()

        out = StringIO()
        call_command(command, stdout=out)
        command_output = out.getvalue().splitlines()[1].strip()

        self.assertEqual(command_output, "Ban caches emptied: 0")
        self.assertEqual(Ban.objects.filter(is_checked=True).count(), 1)

        # expire bans
        expired_date = timezone.now() - timedelta(days=10)
        Ban.objects.all().update(expires_on=expired_date, is_checked=True)
        BanCache.objects.all().update(expires_on=expired_date)

        # invalidate expired ban cache
        out = StringIO()
        call_command(command, stdout=out)
        command_output = out.getvalue().splitlines()[1].strip()

        self.assertEqual(command_output, "Ban caches emptied: 1")
        self.assertEqual(Ban.objects.filter(is_checked=True).count(), 0)

        # see if user is banned anymore
        user.ban_cache = None
        self.assertIsNone(bans.get_user_ban(user, get_cache_versions()))
