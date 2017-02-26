from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from django.utils.six import StringIO

from misago.users import bans
from misago.users.management.commands import invalidatebans
from misago.users.models import Ban, BanCache


UserModel = get_user_model()


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

        self.assertEqual(command_output, 'Bans invalidated: 5')

        self.assertEqual(Ban.objects.filter(is_checked=True).count(), 0)

    def test_bans_caches_updates(self):
        """ban caches are updated"""
        user = UserModel.objects.create_user("Bob", "bob@boberson.com", "Pass.123")

        # ban user
        Ban.objects.create(banned_value="bob")
        user_ban = bans.get_user_ban(user)

        self.assertIsNotNone(user_ban)
        self.assertEqual(Ban.objects.filter(is_checked=True).count(), 1)

        # first call didn't touch ban
        command = invalidatebans.Command()

        out = StringIO()
        call_command(command, stdout=out)
        command_output = out.getvalue().splitlines()[1].strip()

        self.assertEqual(command_output, 'Ban caches emptied: 0')
        self.assertEqual(Ban.objects.filter(is_checked=True).count(), 1)

        # expire bans
        expired_date = timezone.now() - timedelta(days=10)
        Ban.objects.all().update(
            expires_on=expired_date,
            is_checked=True,
        )
        BanCache.objects.all().update(expires_on=expired_date)

        # invalidate expired ban cache
        out = StringIO()
        call_command(command, stdout=out)
        command_output = out.getvalue().splitlines()[1].strip()

        self.assertEqual(command_output, 'Ban caches emptied: 1')
        self.assertEqual(Ban.objects.filter(is_checked=True).count(), 0)

        # see if user is banned anymore
        user = UserModel.objects.get(id=user.id)
        self.assertIsNone(bans.get_user_ban(user))
